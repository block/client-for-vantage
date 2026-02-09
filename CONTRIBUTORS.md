# Contributors Guide

## Development Setup

Install the sdk locally and run tests when you finish making changes:

```bash
uv run nox
```

## Testing

All tests are integration tests that call the actual Vantage API. For an SDK, this is somewhat unavoidable, the primary value is correctness against the actual API rather than testing isolated logic.

### Setting up a sandbox

1. Create a free account at [vantage.sh](https://vantage.sh)
2. Generate an API key from the Vantage console under Settings -> API Access Tokens
3. Copy your workspace token from the URL bar (the `wrkspc_*` value) or from Settings -> Workspaces
4. Copy `.sample.env` to `.env` at the project root and fill in the values:
   ```
   VANTAGE_API_KEY=<your-api-key>
   WORKSPACE_TOKEN=<your-workspace-token>
   ```
5. Verify the setup by running a single test against the live API:
   ```bash
   just test tests/test_main.py::test_get_me
   ```

### Running tests

Use the `just` recipes to run tests locally or in CI:

| Command | Description |
|---|---|
| `just test` | Run tests against the live API |
| `just test-vcr` | Run tests using recorded cassettes (no network) |
| `just test-vcr-record` | Record cassettes for tests that don't have one yet |
| `just test-vcr-rewrite` | Re-record all cassettes from scratch |
| `just test-live` | Run tests against the live API with recording disabled |

Pass additional flags after any command:

```bash
just test -k 'not slow'
just test-vcr-record tests/test_main.py::test_get_dashboard
just test-vcr-rewrite tests/test_main.py::test_get_dashboard
```

Some tests require polling endpoints and take longer to complete:
- Run only slow tests: `just test -- -m slow`
- Exclude slow tests: `just test -- -k 'not slow'`

### How VCR cassette testing works

The test suite uses [pytest-recording](https://github.com/kiwicom/pytest-recording), a pytest plugin wrapping [VCR.py](https://vcrpy.readthedocs.io/), to record and replay HTTP interactions.

When you run tests with `VCR_ENABLED=true`, the following happens:

1. `conftest.py` checks `Settings.vcr_enabled` and auto-applies `@pytest.mark.vcr` to every test via `pytest_collection_modifyitems`
2. `ResourceNameFactory` switches to deterministic names with a `_vcr` suffix (e.g. `test_folder_vcr`) so that request URLs and payloads match the recorded cassettes
3. The session-scoped `vcr_config` fixture configures VCR to:
   - Store YAML cassettes in `tests/cassettes/`
   - Scrub `authorization` headers from recorded requests
   - Strip `Date` and `X-Request-Id` headers from responses
   - Match requests on method, scheme, host, port, path, and query
4. Depending on the `--record-mode` flag:
   - `none` - replay only, fail if no cassette exists (used in CI with `--block-network`)
   - `once` - record if no cassette exists, replay if it does
   - `rewrite` - always re-record, replacing existing cassettes

In CI (`noxfile.py`), when `CI=true` is set, VCR is auto-enabled with `--record-mode=none --block-network` so tests never make real HTTP calls.

### When to re-record cassettes

Re-record cassettes when:
- You add a new test function (use `just test-vcr-record tests/test_main.py::test_your_new_test`)
- An API response schema changes (use `just test-vcr-rewrite tests/test_main.py::test_affected_test`)
- A fixture changes the request payload (field values, resource names, etc.)

## Regenerating Models

`vantage_sdk/models/gen_models/` is generated using the `datamodel-codegen` tool. All codegen configuration lives in `pyproject.toml` under `[tool.datamodel-codegen]`.

> **Important:** Do not manually edit files in `vantage_sdk/models/gen_models/`. Any changes will be overwritten when models are regenerated.

If you encounter type issues, bugs in the generated models, or need to extend functionality:
1. Overload the class in `vantage_sdk/models/common.py` by inheriting from the generated model.
2. Add your overrides (using `# pyright: ignore[reportIncompatibleVariableOverride]` if changing types).
3. Import your new class in `vantage_sdk/models/__init__.py` so it overrides the generated version in the package interface.

See `vantage_sdk/models/common.py` for detailed instructions and examples.

To regenerate the models:

```bash
just generate-models
```

This fetches the latest OpenAPI spec from `https://api.vantage.sh/v2/oas_v3.json` and generates Pydantic v2 models.
