# --- Formatting ---

format:
  uv run ruff format vantage_sdk

# --- Linting ---

lint:
  uv run ruff check --fix vantage_sdk

# --- Testing ---

test *FLAGS:
  uv run pytest {{FLAGS}}

test-vcr *FLAGS:
  VCR_ENABLED=true uv run pytest --record-mode=none --block-network {{FLAGS}}

test-vcr-record *FLAGS:
  VCR_ENABLED=true uv run pytest --record-mode=once {{FLAGS}}

test-vcr-rewrite *FLAGS:
  VCR_ENABLED=true uv run pytest --record-mode=rewrite {{FLAGS}}

test-live *FLAGS:
  uv run pytest --disable-recording {{FLAGS}}

# --- Type Checking ---

typecheck:
  uv run basedpyright vantage_sdk/

typecheck-tests:
  uv run basedpyright tests/

# --- Run all checks ---

check: format lint typecheck test

# --- Code Generation ---

generate-models:
  uv run datamodel-codegen \
    --url https://api.vantage.sh/v2/oas_v3.json \
    --output model.py
