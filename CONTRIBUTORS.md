# Contributors Guide

## Development Setup

Install the sdk locally and run tests when you finish making changes:

```bash
uv run nox
```

## Testing

All tests are integration tests that call the actual Vantage API. For an SDK, this is somewhat unavoidable, the primary value is correctness against the actual API rather than testing isolated logic.

- A Vantage API key and workspace token are required - use `.sample.env` as a template to create your `.env` file
  - **IMPORTANT:** Create a fresh Vantage account at `vantage.sh` and use the API key and workspace token from that account
- Use the `just` recipes to run tests locally or in CI
  - VCR-backed CI run: `just test-vcr`
  - Record VCR cassettes: `just test-vcr-record tests/test_main.py::test_get_dashboard`
  - Rewrite VCR cassettes: `just test-vcr-rewrite tests/test_main.py::test_get_dashboard`
  - Live tests without recording: `just test-live`
- Some tests require polling endpoints and take longer to complete
  - Run these with `just test -- -m slow`
  - Exclude them with `just test -- -k 'not slow'`

## Regenerating Models

`vantage_sdk/models/gen_models/` is generated using the `datamodel-codegen` tool via a JSON file containing the official Vantage API spec.

> **Important:** Do not manually edit files in `vantage_sdk/models/gen_models/`. Any changes will be overwritten when models are regenerated.

If you encounter type issues, bugs in the generated models, or need to extend functionality:
1. Overload the class in `vantage_sdk/models/common.py` by inheriting from the generated model.
2. Add your overrides (using `# pyright: ignore[reportIncompatibleVariableOverride]` if changing types).
3. Import your new class in `vantage_sdk/models/__init__.py` so it overrides the generated version in the package interface.

See `vantage_sdk/models/common.py` for detailed instructions and examples.

To download the latest OpenAPI spec from Vantage:

```bash
just download-openapi
```

To regenerate the models from the downloaded spec:

```bash
just generate-models
```

This command will:
1. Read `openapi_spec.json`
2. Generate Pydantic v2 models with full type safety

## Versioning

Please bump the major version if you make a breaking change, and the minor version if you are making a small change/bug fix. The CI will only upload the library to Artifactory if it encounters a version of the package in the repository that has never been uploaded.
