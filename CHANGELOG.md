# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [1.1.0] - 2026-02-06
### Added
- `get_virtual_tag_processing_status()` method for checking custom tag processing status
- Configurable `timeout` property on `VantageSDK` with getter/setter
- `pytest-recording` (VCR.py wrapper) for cassette-based test playback, toggled via `VCR_ENABLED` env var
- 59 YAML cassettes in `tests/cassettes/` covering all current test functions
- `just test-vcr`, `just test-vcr-record`, `just test-vcr-rewrite`, and `just test-live` commands
- Nox `tests` session auto-enables VCR with `--record-mode=none --block-network` in CI
- Deterministic `_vcr` suffixed resource names in `ResourceNameFactory` when VCR is enabled
- `pytest-timeout` dev dependency

### Changed
- Regenerated models with `parent-scoped-naming = true` in `datamodel-codegen`, replacing generic numbered names (e.g. `Value3Value`, `Settings1Settings`) with descriptive parent-scoped names (e.g. `UpdateVirtualTagConfigValue`, `CreateCostReportSettings`)
- Upgraded `datamodel-code-generator` to `>=0.53.0` with `[http,ruff]` extras and added `formatters = ["ruff-format", "ruff-check"]`
- Moved codegen flags from `justfile` into `pyproject.toml` under `[tool.datamodel-codegen]`
- Code generation now fetches the OpenAPI spec directly via URL instead of downloading to disk; removed `scripts/download_openapi.py`
- Replaced `mypy` with `basedpyright` for type checking in strict mode
- Pinned PyPI index to `https://pypi.org/simple` to prevent corporate proxy injection
- Removed `CostMetric` and `Aggregation` override classes from `common.py` (generated models now have correct types)
- Simplified `_post` and `_put` to always accept `BaseModel` directly

### Fixed
- Adjusted pagination logging to avoid line length lint failures

