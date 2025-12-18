# Contributors Guide

## Development Setup

Install the sdk locally and run tests when you finish making changes:

```bash
uv run nox
```

## Testing

All tests are integration tests that call the actual Vantage API. For an SDK, this is somewhat unavoidable, the primary value is correctness against the actual API rather than testing isolated logic.

- A Vantage API key and workspace token are required - use `.sample.env` as a template to create your `.env` file
  - **IMPORTANT:** Use a sandbox/test workspace token, NOT a production workspace
- Some tests require polling endpoints and take longer to complete
  - Run these with `uv run pytest -m slow`
  - Exclude them with `uv run pytest -k 'not slow'`

## Regenerating Models

`vantage_sdk/models/gen_models/` is generated using the `datamodel-codegen` tool via a JSON file containing the official Vantage API spec.

> **Important:** Do not manually edit files in `vantage_sdk/models/gen_models/`. Any changes will be overwritten when models are regenerated.

If you encounter type issues, bugs in the generated models, or need to extend functionality:
1. Overload the class in `vantage_sdk/models/common.py` by inheriting from the generated model.
2. Add your overrides (using `# type: ignore[assignment]` if changing types).
3. Import your new class in `vantage_sdk/models/__init__.py` so it overrides the generated version in the package interface.

See `vantage_sdk/models/common.py` for detailed instructions and examples.

To download the latest OpenAPI spec from Vantage:

```bash
just download-api
```

To regenerate the models from the downloaded spec:

```bash
just generate-models
```

This command will:
1. Read `openapi_spec.json`
2. Generate Pydantic v2 models with full type safety

### datamodel-codegen Flags Explained

- **`--input-file-type openapi`**  
  Instructs the generator that the input file (or URL) is in OpenAPI format (other options include jsonschema, json, yaml, dict, csv)

- **`--output-model-type pydantic_v2.BaseModel`**  
  Tells the tool to generate models using **Pydantic v2** style classes (`BaseModel` from Pydantic v2)

- **`--target-python-version 3.10`**  
  Generates code compatible with Python 3.10 syntax and features

- **`--use-generic-container-types`**  
  Uses generic collection types like `Sequence[str]` and `Mapping[str, Any]` instead of concrete types like `list[str]` and `dict[str, Any]`

- **`--use-subclass-enum`**  
  If an enum has a type (string, int, etc.), generates an enum class that subclasses that type (e.g., `class Color(str, Enum): ...`) for better type hints and serialization

- **`--use-union-operator`**  
  Enables the `|` operator syntax for unions (PEP 604) instead of `Union[]` (e.g., `str | None` instead of `Union[str, None]`)

- **`--reuse-model`**  
  When identical schemas appear multiple times, creates a single model and reuses it, preventing duplicate class definitions

- **`--use-schema-description`**  
  Uses the `description` field from the OpenAPI spec to populate class docstrings for better documentation

- **`--collapse-root-models`**  
  Merges models that have a root-type field into the models that use them, reducing the number of intermediate wrapper models

- **`--field-constraints`**  
  Uses Pydantic field constraints (like `min_length`, `max_length`) instead of `constr()` style annotations

- **`--use-annotated`**  
  Uses `typing.Annotated` with `Field()` for field definitions, which is the recommended Pydantic v2 style

- **`--strict-nullable`**  
  Treats fields without explicit `nullable: true` as required (non-nullable), following strict OpenAPI interpretation

- **`--use-default-kwarg`**  
  Uses `default=` keyword argument in `Field()` definitions instead of positional arguments for better readability

- **`--parent-scoped-naming`**  
  Names inline models based on their parent context (e.g., `CreateUserAddress` instead of generic `Address1`), making model names more descriptive and avoiding generic numbered suffixes

- **`--openapi-scopes schemas paths parameters`**  
  Specifies which OpenAPI scopes to include in the generated models

## Versioning

Please bump the major version if you make a breaking change, and the minor version if you are making a small change/bug fix. The CI will only upload the library to Artifactory if it encounters a version of the package in the repository that has never been uploaded.
