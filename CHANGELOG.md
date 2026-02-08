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

## [6.0.0] - 2025-07-03
### Added
- Added support for Business Metrics endpoints

## [5.2.0] - 2025-06-27
### Changed
- Migrated from Poetry to UV for faster dependency management and improved developer experience
- Regenerated all Pydantic models using `datamodel-codegen` with improved configuration to fix model duplication issues (e.g., `CreateVirtualTagConfigValue` instead of generic `Value2`)

## [0.3.2] - 2025-04-15
### Added
- Custom json serialization logic for the CreateDataExport pydantic model so that groupings are serialized as a string with values separated by commas 

### Fixed
- Added more detailed error messages for Data Export methods

## [0.3.1] - 2025-04-15
### Fixed
- Fixed bug where error classes were missing parameters in the constructor

## [0.3.0] - 2025-04-07
### Added
- Added data export PUT and GET endpoints
- Created new CreateCostReport model by subclassing the codegen-generated model to implement new field validation logic using Pydantic's model_validator

### Changed
- Regenerated models based on updated OpenAPI specification

### Fixed
- Fixed compatibility issue with Python 3.10 not supporting StrEnum, now using alternative library

### Updated
- Updated tests with new methods

## [0.1.0] - 2025-03-11
### Changed
- Switched to Async + HTTPX for Pagination
- All methods now accept only Pydantic baseclass parameters
- Paginated methods now return a single object rather than a list (e.g., list[CostReport] -> CostReports)

### Added
- Added FolderTokenParams, CostReportTokenParams, SavedFilterTokenParams, and VirtualTagTokenParams Pydantic classes
- Added utility functions for generating unique names and printing client details

### Removed
- Removed back off and auto retry functionality

## [0.0.3] - 2025-02-24
### Fixed
- Fixed `get_cost_report_costs` SDK method

### Added
- Added test for `get_cost_report_costs` SDK method

## [0.0.1]/[0.0.2] - 2025-02-15
### Added
- Initial release
