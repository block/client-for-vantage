# --- Formatting ---

format:
  uv run ruff format vantage_sdk

# --- Linting ---

lint:
  uv run ruff check --fix vantage_sdk

# --- Testing ---

test:
  uv run pytest

# --- Type Checking ---

typecheck:
  uv run mypy

# --- Run all checks ---

check: format lint typecheck test

# --- Code Generation ---

download-openapi:
  uv run python scripts/download_openapi.py

generate-models: download-openapi
  uv run datamodel-codegen \
    --input openapi_spec.json \
    --output vantage_sdk/models/gen_models \
    --input-file-type openapi \
    --output-model-type pydantic_v2.BaseModel \
    --target-python-version 3.10 \
    --use-generic-container-types \
    --use-subclass-enum \
    --use-union-operator \
    --reuse-model \
    --use-schema-description \
    --collapse-root-models \
    --field-constraints \
    --use-annotated \
    --strict-nullable \
    --use-default-kwarg \
    --parent-scoped-naming \
    --openapi-scopes schemas paths parameters