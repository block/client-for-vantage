## Code Architecture

### Project Structure

```
tests
├── __init__.py
├── conftest.py
├── test_main.py
└── test_models.py
vantage_sdk
├── __init__.py
├── client.py
└── models
    ├── __init__.py
    ├── common.py
    └── gen_models
        ├── __init__.py
        └── access_grant.py
noxfile.py
pyproject.toml
openapi_spec.json
```

### Core Components

1. **Client (`VantageSDK` class)** - The main SDK interface in `client.py` that handles all API interactions:
   - Manages API authentication and requests
   - Provides typed methods for all Vantage API endpoints
   - Handles pagination automatically for endpoints that return multiple items
   - Implements parallel request processing for paginated data

2. **Models** - Pydantic v2 models that provide strong typing and validation:
   - Base models in `vantage_sdk/models/common.py`
   - Auto-generated models in `vantage_sdk/models/gen_models/` from the Vantage API OpenAPI spec

3. **Testing** - Comprehensive test suite with fixtures and test cases:
   - Tests for all API endpoints
   - Fixtures for resources like folders, cost reports, filters, etc.
   - Some tests are marked as "slow" due to polling requirements

### Data Flow

1. User initializes the SDK with an API key: `client = VantageSDK(vantage_api_key)`
2. User calls SDK methods with typed parameters: `client.create_cost_report(cost_report)`
3. SDK converts parameters to API format and makes HTTP requests
4. SDK parses responses into typed Pydantic models
5. For paginated responses, SDK handles pagination automatically, potentially using parallel requests

### Error Handling

- HTTP errors are surfaced via `HTTPError` and `HTTPStatusError` from the httpx library
- Type validation errors come from Pydantic's validation system
- Tests verify proper error responses (e.g., 404 when a resource is deleted)

### Notable Features

1. **Pagination Handling** - SDK automatically handles paginated responses using both sequential and parallel request strategies
2. **Type Safety** - All inputs and outputs are validated using Pydantic models
3. **Asynchronous Processing** - Uses asyncio and httpx for efficient parallel request processing
4. **Rate Limit Warning** - Warns users about endpoints with low rate limits

## Development Notes

1. When adding new endpoint methods to the `VantageSDK` class, follow the existing pattern:
   - Use typed Pydantic models for parameters and return values, DO NOT create new models unless necessary, always check if the model already exists in `vantage_sdk/models/gen_models/` before creating a new one.
   - Add appropriate docstrings, respect the Google PyDoc style
   - Use the existing protected methods for making requests (e.g., `_get`, `_post`, `_put`, `_delete`)
   - Use `httpx` for making requests, handle errors with `HTTPStatusError`
   - Consider if the endpoint returns paginated data
   - All method arguments should be typed using Pydantic models, do not use primitive types directly unless absolutely necessary

2. If creating/updating models manually:
   - For complex validation requirements, subclass the auto-generated models and add to `vantage_sdk/models/common.py`
   - Use Pydantic's `Field` for additional constraints and metadata
   - Use `Annotated` for fields that require specific validation or metadata
   - Use Pydantic validators for custom validation logic
   - When API responses return different types than those defined in the generated models, overload the field with the actual type that matches what the API returns, using `Field(default=None)` for nullable fields. For example: `amount: int | None = Field(default=None)  # type: ignore[assignment]` instead of `amount: int | str | None = None  # type: ignore[assignment]` if the API actually returns integers or null

3. When changing the library version:
   - Update the version in `pyproject.toml`
   - Add an entry to `CHANGELOG.md`
   - Follow semantic versioning (major for breaking changes, minor for features, patch for fixes)

4. Testing guidelines:
   - DO NOT add new files to the test directory
   - Only edit existing test files (test_main.py, test_models.py, conftest.py)
   - Add new test cases to the appropriate existing test files
   - After you add a test, run the specific test to verify that it works. DO NOT PROCEED until the test passes.
   - The tests are written to be idempotent, meaning they need to create and delete their own resources, so they can be run multiple times without side effects. Always create fixtures to set up any required resources before creating the tests themselves.
   - If you're implementing a fixture that requires another resource that isn't implemented yet (e.g., access grants need teams), pause and implement the required resource methods first before continuing with the original implementation
   - Refer to the Cost Report tests for examples of how to create fixtures and test cases
   - Do not litter the tests with hasattr() checks, use the `hasattr` function only when absolutely necessary, and prefer using Pydantic's validation features to ensure the models are correctly structured. For example:
   ```
   updated_virtual_tag = vantage_sdk.update_virtual_tag(virtual_tag_token_params, virtual_tag_update_params)

   assert updated_virtual_tag is not None
   ```
   - **IMPORTANT: Setup and teardown logic should ONLY be in fixtures, NEVER in the test functions themselves**
   - **IMPORTANT: Avoid redundant tests - if the fixture already tests create/delete operations, do not create separate test_create_* or test_delete_* functions**
   - **CRITICAL: ALL fixtures MUST follow the exact same structure pattern:**
     1. Create a name using RESOURCES.resource_name property (add a property to TestResources if needed)
     2. Create the resource during setup
     3. Verify the resource was created successfully with assertions
     4. Yield the resource
     5. Delete the resource during teardown
     6. Verify the resource was deleted by attempting to get it and asserting 404 error
   - **IMPORTANT: Even for resources that can't be directly created via API (like tags), you MUST find a way to follow the standard fixture pattern - typically by creating a proxy resource (like a virtual tag) that appears in the target list.**
   
   Example of CORRECT test structure:
   ```python
   # In conftest.py - Fixture handles ALL setup/teardown
   @pytest.fixture()
   def dashboard_fixture(vantage_sdk, cost_report_fixture):
       # Setup - create the resource
       new_dashboard = CreateDashboard(...)
       dashboard = vantage_sdk.create_dashboard(new_dashboard)
       
       yield dashboard
       
       # Teardown - delete the resource
       params = DashboardTokenParams(dashboard_token=dashboard.token)
       vantage_sdk.delete_dashboard(params)
       
       # Verify deletion
       with pytest.raises(HTTPError) as exc_info:
           vantage_sdk.get_dashboard(params)
       assert exc_info.value.response.status_code == 404

   # In test_main.py - Tests ONLY test the specific functionality
   def test_get_dashboard(vantage_sdk, dashboard_fixture):
       params = DashboardTokenParams(dashboard_token=dashboard_fixture.token)
       dashboard = vantage_sdk.get_dashboard(params)
       assert dashboard is not None
       assert dashboard.token == dashboard_fixture.token

   def test_update_dashboard(vantage_sdk, dashboard_fixture):
       params = DashboardTokenParams(dashboard_token=dashboard_fixture.token)
       dashboard_update = UpdateDashboard(title="new_title")
       updated = vantage_sdk.update_dashboard(params, dashboard_update)
       assert updated.title == "new_title"
       
   # NO test_create_dashboard or test_delete_dashboard needed - fixture handles this!
   ```
   
   Example of INCORRECT test structure:
   ```python
   # WRONG - Don't do setup/teardown in test functions
   def test_create_dashboard(vantage_sdk):
       new_dashboard = CreateDashboard(...)  # WRONG - setup in test
       dashboard = vantage_sdk.create_dashboard(new_dashboard)
       
       # Cleanup
       vantage_sdk.delete_dashboard(...)  # WRONG - teardown in test
   
   # WRONG - Redundant test when fixture already tests this
   def test_delete_dashboard(vantage_sdk):
       # Create dashboard
       dashboard = vantage_sdk.create_dashboard(...)  # WRONG - setup in test
       
       # Delete it
       vantage_sdk.delete_dashboard(...)
       
       # Verify
       with pytest.raises(HTTPError):
           vantage_sdk.get_dashboard(...)
   ```

5. Miscellaneous:
   - DO NOT make changes to files annotated with the following comment: `# generated by datamodel-codegen:`
   - Always include import statements at the top of the file, never import modules in the middle of the file
   - After you implement each group of methods, push a commit with the changes and update the `CLAUDE.md` file to indicate that the methods have been implemented
   - Each token param Pydantic class should have a validation method that checks if the token begins with the correct prefix, e.g.:
   ```python
    @field_validator("integration_token", mode="before")
    def validate_integration_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("accss_crdntl"):
            raise ValueError("integration_token must start with 'accss_crdntl'")
        return value
   ```

   ## Testing Against the Live API

   The test suite runs against the live Vantage API at api.vantage.sh. Not all tests will pass on every run.

   ### Transient failures

   Some endpoints are slow or return intermittent server errors (e.g. 502 on paginated requests, timeouts on data export polling). These do not indicate code bugs and may pass on a subsequent run. Do not add `pytest.skip` for these.

   ### Permanently unskippable endpoints

   Some endpoints require account-level configuration that the test environment does not have, such as enterprise permissions, connected Slack/Teams integrations, or email recipients belonging to the organization. Tests for these should use `@pytest.mark.skip(reason="...")` with a short explanation of why they cannot run.

   Only add `pytest.skip` when the test is structurally unable to pass due to missing permissions or infrastructure, not for flaky or slow behavior.