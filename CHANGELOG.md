# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [1.3.1](https://github.com/block/client-for-vantage/compare/v1.3.0...v1.3.1) (2026-03-31)


### Bug Fixes

* use GITHUB_TOKEN instead of missing GitHub App token ([da13ba0](https://github.com/block/client-for-vantage/commit/da13ba0dc600cd40d4fc7b7e5da3c040114597ab))
* use GITHUB_TOKEN instead of missing GitHub App token ([e7a5354](https://github.com/block/client-for-vantage/commit/e7a5354bf88c4c70d4ad27385538ba45c87b2baa))

## [1.3.0](https://github.com/block/client-for-vantage/compare/v1.2.0...v1.3.0) (2026-03-25)


### Features

* remove CostsDataExportsPostParametersQuery in favor of inline groupings ([fa47910](https://github.com/block/client-for-vantage/commit/fa47910f251b4a2c1549abd6de6daa92740cdb57))

## [1.2.0](https://github.com/block/client-for-vantage/compare/v1.1.1...v1.2.0) (2026-03-12)


### Features

* upgrade codegen, refresh models, and add OpenAPI drift check ([3905554](https://github.com/block/client-for-vantage/commit/390555443412a87c7a3dd39914501f37f5b2fd99))


### Documentation

* adding release-please docs ([7d9f181](https://github.com/block/client-for-vantage/commit/7d9f181fda6fb890a7cbd130461b251fdd988820))

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
