# --- Formatting ---

format:
  uv run ruff format vantage_sdk

# --- Linting ---

lint:
  uv run ruff check --fix vantage_sdk

# --- Testing ---

test *FLAGS:
  uv run pytest {{FLAGS}}

# --- Type Checking ---

typecheck:
  uv run basedpyright vantage_sdk/

typecheck-tests:
  uv run basedpyright tests/

# --- Run all checks ---

check: format lint typecheck test

# --- Code Generation ---

download-openapi:
  uv run python scripts/download_openapi.py

generate-models-from-url:
  uv run datamodel-codegen \
    --url https://example.com/api/openapi.yaml \
    --output model.py

generate-models: download-openapi
  uv run datamodel-codegen
