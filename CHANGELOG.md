# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [1.1.0] - 2026-02-06
### Changed
- Regenerated models with updated datamodel-codegen configuration and module split
- Added compatibility aliases for renamed request models and recommendation resource models

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
