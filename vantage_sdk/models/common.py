"""
Module for custom model overrides and extensions.

This module provides a way to override or extend the auto-generated Pydantic models from `gen_models`.
This is necessary when the generated models (derived from the OpenAPI spec) contain bugs, incorrect types,
or missing validation logic that matches the actual API behavior.

How to override a model:
1. Import the generated model as `Original<ModelName>` (e.g., `from .gen_models import CostReport
   as OriginalCostReport`)
2. Define a new class inheriting from the original: `class CostReport(OriginalCostReport):`
3. Override specific fields with corrected types
   - Use `Annotated` and `Field` to preserve descriptions if needed
   - Use `# type: ignore[assignment]` to silence type checkers when narrowing or changing types in a
     way that technically violates the Liskov Substitution Principle but is correct for the data
4. Ensure the new model is exported in `__init__.py` so it replaces the generated one in the package interface.
"""

from collections.abc import Mapping, Sequence
from typing import Annotated, Any

from pydantic import BaseModel, Field, field_serializer, field_validator, model_validator

# ruff: noqa: I001
from vantage_sdk.models.gen_models import (
    BudgetAlert as OriginalBudgetAlert,
    BudgetAlerts as OriginalBudgetAlerts,
    ChartSettings as OriginalChartSettings,
    CostReport as OriginalCostReport,
    CostReports as OriginalCostReports,
    CostsDataExportsPostRequest as OriginalCostsDataExportsPostRequest,
    CostsDataExportsPostRequestSchema,
    CostsDataExportsPostParametersQuery as OriginalCostsDataExportsPostParametersQuery,
    CreateCostReport as OriginalCreateCostReport,
    CreateCostReportSettings as OriginalCreateCostReportSettings,
    DataExport as OriginalDataExport,
    DataExportManifest as OriginalDataExportManifest,
    FinancialCommitment as OriginalFinancialCommitment,
    FinancialCommitments as OriginalFinancialCommitments,
    Recommendation as OriginalRecommendation,
    Recommendations as OriginalRecommendations,
)

# --------------------------------
# Token Parameter Classes
# --------------------------------


class FolderTokenParams(BaseModel):
    """Parameters for endpoints that require a folder token"""

    folder_token: str = Field(..., description="The token for the Folder you want to fetch reports from")

    @field_validator("folder_token", mode="before")
    def validate_folder_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("fldr_"):
            raise ValueError("folder_token must start with 'fldr_'")
        return value


class CostReportTokenParams(BaseModel):
    """Parameters for endpoints that require a cost report token"""

    cost_report_token: str = Field(..., description="The token for the Cost Report you want to access")

    @field_validator("cost_report_token", mode="before")
    def validate_cost_report_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("rprt_"):
            raise ValueError("cost_report_token must start with 'rprt_'")
        return value


class SavedFilterTokenParams(BaseModel):
    """Parameters for endpoints that require a saved filter token"""

    saved_filter_token: str = Field(..., description="The token for the Saved Filter you want to access")

    @field_validator("saved_filter_token", mode="before")
    def validate_saved_filter_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("svd_fltr_"):
            raise ValueError("saved_filter_token must start with 'svd_fltr_'")
        return value


class VirtualTagTokenParams(BaseModel):
    """Parameters for endpoints that require a virtual tag token"""

    virtual_tag_token: str = Field(..., description="The token for the Virtual Tag you want to access")

    @field_validator("virtual_tag_token", mode="before")
    def validate_virtual_tag_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("vtag_"):
            raise ValueError("virtual_tag_token must start with 'vtag'")
        return value


class DataExportTokenParams(BaseModel):
    """Parameters for endpoints that require a data export token"""

    data_export_token: str = Field(..., description="The token for the data export you want to access")

    @field_validator("data_export_token", mode="before")
    def validate_data_export_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("dta_xprt"):
            raise ValueError("data_export_token must start with 'dta_xprt'")
        return value


class BusinessMetricTokenParams(BaseModel):
    """Parameters for endpoints that require a business metric token"""

    business_metric_token: str = Field(..., description="The token for the business metric you want to access")

    @field_validator("business_metric_token", mode="before")
    def validate_business_metric_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("bsnss_mtrc_"):
            raise ValueError("business_metric_token must start with 'bsnss_mtrc_'")
        return value


class IntegrationTokenParams(BaseModel):
    """Parameters for endpoints that require an integration token"""

    integration_token: str = Field(..., description="The token for the Integration you want to access")

    @field_validator("integration_token", mode="before")
    def validate_integration_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("accss_crdntl"):
            raise ValueError("integration_token must start with 'accss_crdntl'")
        return value


class AccessGrantTokenParams(BaseModel):
    """Parameters for endpoints that require an access grant token"""

    access_grant_token: str = Field(..., description="The token for the Access Grant you want to access")

    @field_validator("access_grant_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'rsrc_accss_grnt_'."""
        if not value.startswith("rsrc_accss_grnt_"):
            raise ValueError("access_grant_token must start with 'rsrc_accss_grnt_'")
        return value


class TeamTokenParams(BaseModel):
    """Parameters for endpoints that require a team token"""

    team_token: str = Field(..., description="The token for the Team you want to access")

    @field_validator("team_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'team_'."""
        if not value.startswith("team_"):
            raise ValueError("team_token must start with 'team_'")
        return value


class AnomalyAlertTokenParams(BaseModel):
    """Parameters for endpoints that require an anomaly alert token"""

    anomaly_alert_token: str = Field(..., description="The token for the Anomaly Alert you want to access")

    @field_validator("anomaly_alert_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'anmly_alrt_'."""
        if not value.startswith("anmly_alrt_"):
            raise ValueError("anomaly_alert_token must start with 'anmly_alrt_'")
        return value


class AnomalyNotificationTokenParams(BaseModel):
    """Parameters for endpoints that require an anomaly notification token"""

    anomaly_notification_token: str = Field(
        ..., description="The token for the Anomaly Notification you want to access"
    )

    @field_validator("anomaly_notification_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'rprt_alrt'."""
        if not value.startswith("rprt_alrt"):
            raise ValueError("anomaly_notification_token must start with 'rprt_alrt'")
        return value


class BillingRuleTokenParams(BaseModel):
    """Parameters for endpoints that require a billing rule token"""

    billing_rule_token: str = Field(..., description="The token for the Billing Rule you want to access")

    @field_validator("billing_rule_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'bllng_rule_'."""
        if not value.startswith("bllng_rule_"):
            raise ValueError("billing_rule_token must start with 'bllng_rule_'")
        return value


class BudgetTokenParams(BaseModel):
    """Parameters for endpoints that require a budget token"""

    budget_token: str = Field(..., description="The token for the Budget you want to access")

    @field_validator("budget_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'bdgt_'."""
        if not value.startswith("bdgt_"):
            raise ValueError("budget_token must start with 'bdgt_'")
        return value


class BudgetAlertTokenParams(BaseModel):
    """Parameters for endpoints that require a budget alert token"""

    budget_alert_token: str = Field(..., description="The token for the Budget Alert you want to access")

    @field_validator("budget_alert_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'bdgt_alrt_'."""
        if not value.startswith("bdgt_alrt_"):
            raise ValueError("budget_alert_token must start with 'bdgt_alrt_'")
        return value


class WorkspaceTokenParams(BaseModel):
    """Parameters for endpoints that require a workspace token"""

    workspace_token: str | None = Field(
        None,
        description=(
            "The token of the Workspace to list resources for. "
            "Required if the API token is associated with multiple Workspaces."
        ),
    )

    @field_validator("workspace_token", mode="before")
    def validate_token(cls, value: str | None) -> str | None:
        """Validate that the token starts with 'ws_' or 'wrkspc_' if provided."""
        if value is not None and not (value.startswith("ws_") or value.startswith("wrkspc_")):
            raise ValueError("workspace_token must start with 'ws_' or 'wrkspc_'")
        return value


class CostAlertTokenParams(BaseModel):
    """Parameters for endpoints that require a cost alert token"""

    cost_alert_token: str = Field(..., description="The token for the Cost Alert you want to access")

    @field_validator("cost_alert_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'cst_alrt_' or 'cstm_alrt_rl_'."""
        if not (value.startswith("cst_alrt_") or value.startswith("cstm_alrt_rl_")):
            raise ValueError("cost_alert_token must start with 'cst_alrt_' or 'cstm_alrt_rl_'")
        return value


class CostAlertEventTokenParams(BaseModel):
    """Parameters for endpoints that require a cost alert event token"""

    event_token: str = Field(..., description="The token for the Cost Alert Event you want to access")

    @field_validator("event_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'cst_alrt_evnt_'."""
        if not value.startswith("cst_alrt_evnt_"):
            raise ValueError("event_token must start with 'cst_alrt_evnt_'")
        return value


class DashboardTokenParams(BaseModel):
    """Parameters for endpoints that require a dashboard token"""

    dashboard_token: str = Field(..., description="The token for the Dashboard you want to access")

    @field_validator("dashboard_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'dshbrd_'."""
        if not value.startswith("dshbrd_"):
            raise ValueError("dashboard_token must start with 'dshbrd_'")
        return value


class FinancialCommitmentReportTokenParams(BaseModel):
    """Parameters for endpoints that require a financial commitment report token"""

    financial_commitment_report_token: str = Field(
        ..., description="The token for the Financial Commitment Report you want to access"
    )

    @field_validator("financial_commitment_report_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'fncl_cmnt_rprt_'."""
        if not value.startswith("fncl_cmnt_rprt_"):
            raise ValueError("financial_commitment_report_token must start with 'fncl_cmnt_rprt_'")
        return value


class KubernetesEfficiencyReportTokenParams(BaseModel):
    """Parameters for endpoints that require a kubernetes efficiency report token"""

    kubernetes_efficiency_report_token: str = Field(
        ..., description="The token for the Kubernetes Efficiency Report you want to access"
    )

    @field_validator("kubernetes_efficiency_report_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'kbnts_eff_rprt_'."""
        if not value.startswith("kbnts_eff_rprt_"):
            raise ValueError("kubernetes_efficiency_report_token must start with 'kbnts_eff_rprt_'")
        return value


class ManagedAccountTokenParams(BaseModel):
    """Parameters for endpoints that require a managed account token"""

    managed_account_token: str = Field(..., description="The token for the Managed Account you want to access")

    @field_validator("managed_account_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'acct_'."""
        if not value.startswith("acct_"):
            raise ValueError("managed_account_token must start with 'acct_'")
        return value


class NetworkFlowReportTokenParams(BaseModel):
    """Parameters for endpoints that require a network flow report token"""

    network_flow_report_token: str = Field(..., description="The token for the Network Flow Report you want to access")

    @field_validator("network_flow_report_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'ntwrk_flw_rprt_' or 'ntflw_lg_rprt_'."""
        if not (value.startswith("ntwrk_flw_rprt_") or value.startswith("ntflw_lg_rprt_")):
            raise ValueError("network_flow_report_token must start with 'ntwrk_flw_rprt_' or 'ntflw_lg_rprt_'")
        return value


class ProductIdParams(BaseModel):
    """Parameters for endpoints that require a product ID"""

    id: str = Field(..., description="The ID of the product")


class ProductPriceIdParams(BaseModel):
    """Parameters for endpoints that require a product price ID"""

    id: str = Field(..., description="The ID of the price")


class RecommendationTokenParams(BaseModel):
    """Parameters for endpoints that require a recommendation token"""

    recommendation_token: str = Field(..., description="The token for the Recommendation you want to access")

    @field_validator("recommendation_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'rcmndtn_'."""
        if not value.startswith("rcmndtn_"):
            raise ValueError("recommendation_token must start with 'rcmndtn_'")
        return value


class RecommendationResourceTokenParams(BaseModel):
    """Parameters for endpoints that require a recommendation resource token"""

    resource_token: str = Field(..., description="The token for the Recommendation Resource you want to access")

    @field_validator("resource_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'rcmndtn_rsrc_'."""
        if not value.startswith("rcmndtn_rsrc_"):
            raise ValueError("resource_token must start with 'rcmndtn_rsrc_'")
        return value


class ReportNotificationTokenParams(BaseModel):
    """Parameters for endpoints that require a report notification token"""

    report_notification_token: str = Field(..., description="The token for the Report Notification you want to access")

    @field_validator("report_notification_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'rprt_ntfctn_'."""
        if not value.startswith("rprt_ntfctn_"):
            raise ValueError("report_notification_token must start with 'rprt_ntfctn_'")
        return value


class ResourceReportTokenParams(BaseModel):
    """Parameters for endpoints that require a resource report token"""

    resource_report_token: str = Field(..., description="The token for the Resource Report you want to access")

    @field_validator("resource_report_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'prvdr_rsrc_rprt_' or 'rsrc_rprt_'."""
        if not (value.startswith("prvdr_rsrc_rprt_") or value.startswith("rsrc_rprt_")):
            raise ValueError("resource_report_token must start with 'rsrc_rprt_' or 'prvdr_rsrc_rprt_'")
        return value


class ResourceTokenParams(BaseModel):
    """Parameters for endpoints that require a resource token"""

    resource_token: str = Field(..., description="The token for the Resource you want to access")

    @field_validator("resource_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with a valid resource prefix."""
        valid_prefixes = ["prvdr_rsrc_", "fldr_", "rprt_", "bdgt_"]
        if not any(value.startswith(prefix) for prefix in valid_prefixes):
            raise ValueError(f"resource_token must start with one of these prefixes: {', '.join(valid_prefixes)}")
        return value


class SegmentTokenParams(BaseModel):
    """Parameters for endpoints that require a segment token"""

    segment_token: str = Field(..., description="The token for the Segment you want to access")

    @field_validator("segment_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'sgmnt_'."""
        if not value.startswith("sgmnt_"):
            raise ValueError("segment_token must start with 'sgmnt_'")
        return value


class TagKeyParams(BaseModel):
    """Parameters for endpoints that require a tag key"""

    key: str = Field(..., description="The key of the tag")


class UserTokenParams(BaseModel):
    """Parameters for endpoints that require a user token"""

    user_token: str = Field(..., description="The token for the User you want to access")

    @field_validator("user_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'user_' or 'usr_'."""
        if not (value.startswith("user_") or value.startswith("usr_")):
            raise ValueError("user_token must start with 'user_' or 'usr_'")
        return value


class AuditLogTokenParams(BaseModel):
    """Parameters for endpoints that require an audit log token"""

    audit_log_token: str = Field(..., description="The token for the Audit Log you want to access")

    @field_validator("audit_log_token", mode="before")
    def validate_token(cls, value: str) -> str:
        """Validate that the token starts with 'adt_lg_'."""
        if not value.startswith("adt_lg_"):
            raise ValueError("audit_log_token must start with 'adt_lg_'")
        return value


class CreateCostReport(OriginalCreateCostReport):
    """
    CreateCostReport model with additional validation

    This model inherits from the original CreateCostReport model and adds additional validation
    for the start_date, end_date, and date_interval fields.

    The model ensures that either start_date and end_date are provided, or date_interval is provided
    It also ensures that if start_date and end_date are provided, date_interval cannot be provided
    """

    previous_period_end_date: str | None = Field(  # type: ignore[assignment]
        None,
        description="The previous period end date of the CostReport. ISO 8601 Formatted",
    )
    end_date: str | None = Field(  # type: ignore[assignment]
        None,
        description="The end date of the CostReport. ISO 8601 Formatted. Incompatible with 'date_interval' parameter",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_class_attributes(cls, values: dict[str, Any]) -> dict[str, Any]:  # noqa: D102
        start_date: str | None = values.get("start_date")
        end_date: str | None = values.get("end_date")
        date_interval: str | None = values.get("date_interval")

        if (start_date is None or end_date is None) and date_interval is None:
            raise ValueError("Either start_date and end_date must be provided, or date_interval must be provided")

        if start_date and end_date and date_interval:
            raise ValueError("Cannot provide both start_date/end_date and date_interval")

        return values


class DataExportManifest(OriginalDataExportManifest):
    """Corrected DataExportManifest that properly handles the files field as a list of strings"""

    files: Sequence[str] | None = Field(None, examples=[["https://example.com/file1.csv"]])  # type: ignore[assignment]


class DataExport(OriginalDataExport):
    """Corrected DataExport model that properly handles the manifest and attributes fields"""

    manifest: DataExportManifest | None = None  # type: ignore[assignment]
    attributes: Mapping[str, Any] | None = None  # type: ignore[assignment]


class CostsDataExportsPostParametersQuery(OriginalCostsDataExportsPostParametersQuery):
    """Parameters for the Costs Data Exports POST request"""

    groupings: Sequence[str] | None = None

    @field_serializer("groupings", when_used="always")
    def _serialize_groupings(self, groupings: Sequence[str] | None) -> str | None:
        return ",".join(groupings) if groupings else None


class CreateCostReportSettings(OriginalCreateCostReportSettings):
    """Extends CreateCostReportSettings to handle None for 'unallocated' field"""

    @field_validator("unallocated", mode="before")
    def handle_none_unallocated(cls, v: None | bool) -> bool:
        """Handles None value for 'unallocated' field, returning False if None"""
        return False if v is None else v


class ChartSettings(OriginalChartSettings):
    """Extends ChartSettings to fix x_axis_dimension type"""

    x_axis_dimension: Annotated[
        Sequence[str] | None,
        Field(
            description=(
                "The dimension used to group or label data along the x-axis "
                "(e.g., by date, region, or service). NOTE: Only one value is allowed at this time. "
                "Defaults to ['date']."
            )
        ),
    ] = None  # type: ignore[assignment]


class CostReport(OriginalCostReport):
    """Extends OriginalCostReport to include settings field"""

    settings: CreateCostReportSettings | None = None  # type: ignore[assignment]
    chart_settings: ChartSettings | None = None  # type: ignore[assignment]


class CostReports(OriginalCostReports):
    """Extends OriginalCostReports to handle the cost_reports field as a list of CostReport objects"""

    cost_reports: Sequence[CostReport] = Field(default_factory=list)  # type: ignore[assignment]


class BudgetAlert(OriginalBudgetAlert):
    """Extends OriginalBudgetAlert to match API response types"""

    threshold: int | None = None  # type: ignore[assignment]
    duration_in_days: int | None = None  # type: ignore[assignment]
    recipient_channels: Sequence[str] | None = None  # type: ignore[assignment]


class BudgetAlerts(OriginalBudgetAlerts):
    """Extends OriginalBudgetAlerts to handle the budget_alerts field as a list of BudgetAlert objects"""

    budget_alerts: Sequence[BudgetAlert] = Field(default_factory=list)  # type: ignore[assignment]


# --------------------------------
# Model Extensions
# --------------------------------


class RecommendationResource(BaseModel):
    """RecommendationResource model

    This class represents a resource associated with a recommendation
    """

    token: str | None = None
    arn: str | None = None
    name: str | None = None
    resource_id: str | None = None
    recommendation_token: str | None = None
    account_id: str | None = None
    region: str | None = None
    details: dict | None = None


class RecommendationResources(BaseModel):
    """RecommendationResources model

    This class represents a collection of recommendation resources.
    """

    recommendation_resources: Sequence[RecommendationResource] = Field(default_factory=list)


class FinancialCommitment(OriginalFinancialCommitment):
    """Extends OriginalFinancialCommitment to handle mismatched field types"""

    amount: int | None = Field(default=None)  # type: ignore[assignment]


class FinancialCommitments(OriginalFinancialCommitments):
    """Extends OriginalFinancialCommitments to use the custom FinancialCommitment model"""

    financial_commitments: Sequence[FinancialCommitment] = Field(default_factory=list)  # type: ignore[assignment]


class Recommendation(OriginalRecommendation):
    """Extends OriginalRecommendation to handle mismatched field types"""

    resources_affected_count: int | None = Field(default=None)  # type: ignore[assignment]


class Recommendations(OriginalRecommendations):
    """Extends OriginalRecommendations to use the custom Recommendation model"""

    recommendations: Sequence[Recommendation] = Field(default_factory=list)  # type: ignore[assignment]


class CostsDataExportsPostRequest(OriginalCostsDataExportsPostRequest):
    """Extends OriginalCostsDataExportsPostRequest to use the proper enum for schema_"""

    schema_: Annotated[
        CostsDataExportsPostRequestSchema,
        Field(alias="schema", description="The schema of the data export."),
    ] = CostsDataExportsPostRequestSchema.focus  # type: ignore[assignment]
