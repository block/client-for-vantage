"""
Module for custom model overrides and extensions

This module provides a way to override or extend the auto-generated Pydantic models from `gen_models`
This is necessary when the generated models (derived from the OpenAPI spec) contain bugs, incorrect types,
or missing validation logic that matches the actual API behavior

How to override a model:
1. Import the generated model as `Original<ModelName>`
   Example: `from .gen_models import CostReport as OriginalCostReport`
2. Define a new class inheriting from the original: `CostReport(OriginalCostReport)`
3. Override specific fields with corrected types
   - Use `Field` to preserve descriptions if needed
   - Use `# type: ignore[assignment]` to silence type checkers when narrowing or changing types in a
     way that technically violates the Liskov Substitution Principle but is correct for the data
4. Ensure the new model is exported in `__init__.py` so it replaces the generated one in the package interface
"""

from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel, Field, field_serializer, field_validator, model_validator

# ruff: noqa: I001
from vantage_sdk.models.gen_models import (
    me as me_model,
    resource as resource_model,
    resources as resources_model,
    business_metric as business_metric_model,
    budget_period as budget_period_model,
    budget as budget_model,
    budgets as budgets_model,
    anomaly_notification as anomaly_notification_model,
    anomaly_notifications as anomaly_notifications_model,
    aggregation as aggregation_model,
    settings as settings_model,
    create_budget_alert as create_budget_alert_model,
    budget_alert as budget_alert_model,
    budget_alerts as budget_alerts_model,
    business_metrics as business_metrics_model,
    chart_settings as chart_settings_model,
    cost_report as cost_report_model,
    cost_alert as cost_alert_model,
    cost_metric as cost_metric_model,
    virtual_tag_config_value_cost_metric_aggregation as virtual_tag_config_value_cost_metric_aggregation_model,
    cost_alerts as cost_alerts_model,
    cost_reports as cost_reports_model,
    costs_data_exports_post_parameters_query as costs_data_exports_post_parameters_query_model,
    create_cost_export as create_cost_export_model,
    create_cost_report as create_cost_report_model,
    create_financial_commitment_report as create_financial_commitment_report_model,
    create_kubernetes_efficiency_report as create_kubernetes_efficiency_report_model,
    create_network_flow_report as create_network_flow_report_model,
    create_resource_report as create_resource_report_model,
    create_unit_costs_export as create_unit_costs_export_model,
    data_export as data_export_model,
    data_export_manifest as data_export_manifest_model,
    value2 as value2_model,
    virtual_tag_config_value_cost_metric as virtual_tag_config_value_cost_metric_model,
    provider_resource as provider_resource_model,
    recommendation as recommendation_model,
    recommendation_provider_resources as recommendation_provider_resources_model,
    recommendations as recommendations_model,
    update_budget_alert as update_budget_alert_model,
    update_integration as update_integration_model,
    update_workspace as update_workspace_model,
)

VirtualTagConfigValueCostMetricAggregation = virtual_tag_config_value_cost_metric_aggregation_model.VirtualTagConfigValueCostMetricAggregation

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
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("rsrc_accss_grnt_"):
            raise ValueError("access_grant_token must start with 'rsrc_accss_grnt_'")
        return value


class TeamTokenParams(BaseModel):
    """Parameters for endpoints that require a team token"""

    team_token: str = Field(..., description="The token for the Team you want to access")

    @field_validator("team_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("team_"):
            raise ValueError("team_token must start with 'team_'")
        return value


class AnomalyAlertTokenParams(BaseModel):
    """Parameters for endpoints that require an anomaly alert token"""

    anomaly_alert_token: str = Field(..., description="The token for the Anomaly Alert you want to access")

    @field_validator("anomaly_alert_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("anmly_alrt_"):
            raise ValueError("anomaly_alert_token must start with 'anmly_alrt_'")
        return value


class AnomalyNotificationTokenParams(BaseModel):
    """Parameters for endpoints that require an anomaly notification token"""

    anomaly_notification_token: str = Field(
        ..., description="The token for the Anomaly Notification you want to access"
    )

    @field_validator("anomaly_notification_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("rprt_alrt"):
            raise ValueError("anomaly_notification_token must start with 'rprt_alrt'")
        return value


class BillingRuleTokenParams(BaseModel):
    """Parameters for endpoints that require a billing rule token"""

    billing_rule_token: str = Field(..., description="The token for the Billing Rule you want to access")

    @field_validator("billing_rule_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("bllng_rule_"):
            raise ValueError("billing_rule_token must start with 'bllng_rule_'")
        return value


class BudgetTokenParams(BaseModel):
    """Parameters for endpoints that require a budget token"""

    budget_token: str = Field(..., description="The token for the Budget you want to access")

    @field_validator("budget_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("bdgt_"):
            raise ValueError("budget_token must start with 'bdgt_'")
        return value


class BudgetAlertTokenParams(BaseModel):
    """Parameters for endpoints that require a budget alert token"""

    budget_alert_token: str = Field(..., description="The token for the Budget Alert you want to access")

    @field_validator("budget_alert_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
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
    def validate_token(cls, value: str | None) -> str | None:  # noqa: D102
        if value is not None and not (value.startswith("ws_") or value.startswith("wrkspc_")):
            raise ValueError("workspace_token must start with 'ws_' or 'wrkspc_'")
        return value


class CostAlertTokenParams(BaseModel):
    """Parameters for endpoints that require a cost alert token"""

    cost_alert_token: str = Field(..., description="The token for the Cost Alert you want to access")

    @field_validator("cost_alert_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not (value.startswith("cst_alrt_") or value.startswith("cstm_alrt_rl_")):
            raise ValueError("cost_alert_token must start with 'cst_alrt_' or 'cstm_alrt_rl_'")
        return value


class CostAlertEventTokenParams(BaseModel):
    """Parameters for endpoints that require a cost alert event token"""

    event_token: str = Field(..., description="The token for the Cost Alert Event you want to access")

    @field_validator("event_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("cst_alrt_evnt_"):
            raise ValueError("event_token must start with 'cst_alrt_evnt_'")
        return value


class DashboardTokenParams(BaseModel):
    """Parameters for endpoints that require a dashboard token"""

    dashboard_token: str = Field(..., description="The token for the Dashboard you want to access")

    @field_validator("dashboard_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("dshbrd_"):
            raise ValueError("dashboard_token must start with 'dshbrd_'")
        return value


class FinancialCommitmentReportTokenParams(BaseModel):
    """Parameters for endpoints that require a financial commitment report token"""

    financial_commitment_report_token: str = Field(
        ..., description="The token for the Financial Commitment Report you want to access"
    )

    @field_validator("financial_commitment_report_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("fncl_cmnt_rprt_"):
            raise ValueError("financial_commitment_report_token must start with 'fncl_cmnt_rprt_'")
        return value


class KubernetesEfficiencyReportTokenParams(BaseModel):
    """Parameters for endpoints that require a kubernetes efficiency report token"""

    kubernetes_efficiency_report_token: str = Field(
        ..., description="The token for the Kubernetes Efficiency Report you want to access"
    )

    @field_validator("kubernetes_efficiency_report_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("kbnts_eff_rprt_"):
            raise ValueError("kubernetes_efficiency_report_token must start with 'kbnts_eff_rprt_'")
        return value


class ManagedAccountTokenParams(BaseModel):
    """Parameters for endpoints that require a managed account token"""

    managed_account_token: str = Field(..., description="The token for the Managed Account you want to access")

    @field_validator("managed_account_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("acct_"):
            raise ValueError("managed_account_token must start with 'acct_'")
        return value


class NetworkFlowReportTokenParams(BaseModel):
    """Parameters for endpoints that require a network flow report token"""

    network_flow_report_token: str = Field(..., description="The token for the Network Flow Report you want to access")

    @field_validator("network_flow_report_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
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
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("rcmndtn_"):
            raise ValueError("recommendation_token must start with 'rcmndtn_'")
        return value

class RecommendationResourceTokenParams(BaseModel):
    """Parameters for endpoints that require a recommendation resource token"""

    resource_token: str = Field(..., description="The token for the Recommendation Resource you want to access")

    @field_validator("resource_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("rcmndtn_rsrc_"):
            raise ValueError("resource_token must start with 'rcmndtn_rsrc_'")
        return value


class ReportNotificationTokenParams(BaseModel):
    """Parameters for endpoints that require a report notification token"""

    report_notification_token: str = Field(..., description="The token for the Report Notification you want to access")

    @field_validator("report_notification_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("rprt_ntfctn_"):
            raise ValueError("report_notification_token must start with 'rprt_ntfctn_'")
        return value


class ResourceReportTokenParams(BaseModel):
    """Parameters for endpoints that require a resource report token"""

    resource_report_token: str = Field(..., description="The token for the Resource Report you want to access")

    @field_validator("resource_report_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not (value.startswith("prvdr_rsrc_rprt_") or value.startswith("rsrc_rprt_")):
            raise ValueError("resource_report_token must start with 'rsrc_rprt_' or 'prvdr_rsrc_rprt_'")
        return value


class ResourceTokenParams(BaseModel):
    """Parameters for endpoints that require a resource token"""

    resource_token: str = Field(..., description="The token for the Resource you want to access")

    @field_validator("resource_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        valid_prefixes = ["prvdr_rsrc_", "rsrc_"]
        if not any(value.startswith(prefix) for prefix in valid_prefixes):
            raise ValueError(f"resource_token must start with one of these prefixes: {', '.join(valid_prefixes)}")
        return value


class SegmentTokenParams(BaseModel):
    """Parameters for endpoints that require a segment token"""

    segment_token: str = Field(..., description="The token for the Segment you want to access")

    @field_validator("segment_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
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
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not (value.startswith("user_") or value.startswith("usr_")):
            raise ValueError("user_token must start with 'user_' or 'usr_'")
        return value


class AuditLogTokenParams(BaseModel):
    """Parameters for endpoints that require an audit log token"""

    audit_log_token: str = Field(..., description="The token for the Audit Log you want to access")

    @field_validator("audit_log_token", mode="before")
    def validate_token(cls, value: str) -> str:  # noqa: D102
        if not value.startswith("adt_lg_"):
            raise ValueError("audit_log_token must start with 'adt_lg_'")
        return value

# --------------------------------
# Model Overrides
# --------------------------------

class Resource(resource_model.Resource):
    """Resource model override"""

    metadata: Mapping[str, Any] | None = None  # type: ignore[assignment]

class Resources(resources_model.Resources):
    """Resources model override"""

    resources: Sequence[Resource]  # type: ignore[assignment]


class CreateFinancialCommitmentReport(create_financial_commitment_report_model.CreateFinancialCommitmentReport):
    """Extends CreateFinancialCommitmentReport to allow string dates"""

    start_date: str | None = None  # type: ignore[assignment]
    end_date: str | None = None  # type: ignore[assignment]

class CreateKubernetesEfficiencyReport(create_kubernetes_efficiency_report_model.CreateKubernetesEfficiencyReport):
    """Extends CreateKubernetesEfficiencyReport to allow string dates"""

    start_date: str | None = None  # type: ignore[assignment]
    end_date: str | None = None  # type: ignore[assignment]

class CreateNetworkFlowReport(create_network_flow_report_model.CreateNetworkFlowReport):
    """Extends CreateNetworkFlowReport to allow string dates"""

    start_date: str | None = None  # type: ignore[assignment]
    end_date: str | None = None  # type: ignore[assignment]

class CreateResourceReport(create_resource_report_model.CreateResourceReport):
    """Extends CreateResourceReport to allow nullable titles"""

    title: str | None = None  # type: ignore[assignment]

class CreateCostReport(create_cost_report_model.CreateCostReport):
    """
    CreateCostReport model with additional validation

    This model inherits from the original CreateCostReport model and adds additional validation
    for the start_date, end_date, and date_interval fields

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
        previous_period_start_date: str | None = values.get("previous_period_start_date")
        previous_period_end_date: str | None = values.get("previous_period_end_date")

        if (start_date is None or end_date is None) and date_interval is None:
            raise ValueError("Either start_date and end_date must be provided, or date_interval must be provided")

        if start_date and end_date and date_interval:
            raise ValueError("Cannot provide both start_date/end_date and date_interval")

        if (previous_period_start_date is None) != (previous_period_end_date is None):
            raise ValueError("previous_period_start_date and previous_period_end_date must be provided together")

        return values


class DataExportManifest(data_export_manifest_model.DataExportManifest):
    """Corrected DataExportManifest that properly handles the files field as a list of strings"""

    files: Sequence[str] | None = Field(None, examples=[["https://example.com/file1.csv"]])  # type: ignore[assignment]


class DataExport(data_export_model.DataExport):
    """Corrected DataExport model that properly handles the manifest and attributes fields"""

    manifest: DataExportManifest | None = None  # type: ignore[assignment]
    attributes: Mapping[str, Any] | None = None  # type: ignore[assignment]


class CostsDataExportsPostParametersQuery(
    costs_data_exports_post_parameters_query_model.CostsDataExportsPostParametersQuery
):
    """Parameters for the Costs Data Exports POST request"""

    groupings: Sequence[str] | None = None

    @field_serializer("groupings", when_used="always")
    def _serialize_groupings(self, groupings: Sequence[str] | None) -> str | None:
        return ",".join(groupings) if groupings else None


class CostsDataExportsPostRequest(create_cost_export_model.CreateCostExport):
    """Alias for CreateCostExport model"""

    @model_validator(mode="before")
    @classmethod
    def validate_request(cls, values: dict[str, Any]) -> dict[str, Any]:  # noqa: D102
        cost_report_token = values.get("cost_report_token")
        vql_filter = values.get("filter")
        workspace_token = values.get("workspace_token")
        start_date = values.get("start_date")
        end_date = values.get("end_date")

        if cost_report_token and vql_filter:
            raise ValueError("filter cannot be provided when cost_report_token is set")

        if vql_filter and not workspace_token:
            raise ValueError("workspace_token is required when filter is provided")

        if (start_date is None) != (end_date is None):
            raise ValueError("start_date and end_date must be provided together")

        return values


class UnitCostsDataExportsPostRequest(create_unit_costs_export_model.CreateUnitCostsExport):
    """Extends CreateUnitCostsExport to allow test-only payloads"""

    cost_report_token: str | None = None  # type: ignore[assignment]
    workspace_token: str | None = None  # type: ignore[assignment]
    start_date: str | None = None  # type: ignore[assignment]
    end_date: str | None = None  # type: ignore[assignment]


class BudgetAlertsPostRequest(create_budget_alert_model.CreateBudgetAlert):
    """Extends CreateBudgetAlert to accept integer durations"""

    duration_in_days: int | str | None = None  # type: ignore[assignment]
    workspace_token: str | None = None


class BudgetAlertsBudgetAlertTokenPutRequest(update_budget_alert_model.UpdateBudgetAlert):
    """Alias for UpdateBudgetAlert model"""

class CostAlert(cost_alert_model.CostAlert):
    """Extends CostAlert to allow optional notification fields"""

    email_recipients: Sequence[str] | None = None  # type: ignore[assignment]
    slack_channels: Sequence[str] | None = None  # type: ignore[assignment]
    teams_channels: Sequence[str] | None = None  # type: ignore[assignment]
    minimum_threshold: float | None = None  # type: ignore[assignment]

class CostAlerts(cost_alerts_model.CostAlerts):
    """Extends CostAlerts to use the custom CostAlert model"""

    cost_alerts: Sequence[CostAlert]  # type: ignore[assignment]


class CostMetric(cost_metric_model.CostMetric):
    """Extends CostMetric to allow virtual tag aggregation model"""

    aggregation: VirtualTagConfigValueCostMetricAggregation | aggregation_model.Aggregation | None = None  # type: ignore[assignment]

class IntegrationsIntegrationTokenPutRequest(update_integration_model.UpdateIntegration):
    """Alias for UpdateIntegration model"""


class WorkspacesWorkspaceTokenPutRequest(update_workspace_model.UpdateWorkspace):
    """Alias for UpdateWorkspace model"""

class VirtualTagConfigValueCostMetric(virtual_tag_config_value_cost_metric_model.VirtualTagConfigValueCostMetric):
    """Extends VirtualTagConfigValueCostMetric to allow nullable filters"""

    filter: str | None = None  # type: ignore[assignment]

class Value(value2_model.Value):
    """Extends Value to use virtual tag cost metric models

    The fields ``name``, ``cost_metric``, and ``percentages`` are mutually
    exclusive according to the Vantage API
    """

    cost_metric: VirtualTagConfigValueCostMetric | None = None  # type: ignore[assignment]

    @model_validator(mode="before")
    @classmethod
    def validate_mutually_exclusive_fields(cls, values: dict[str, Any]) -> dict[str, Any]:  # noqa: D102
        exclusive_fields = ["name", "cost_metric", "percentages"]
        provided = [f for f in exclusive_fields if values.get(f) is not None]
        if len(provided) > 1:
            raise ValueError(f"{', '.join(provided)} are mutually exclusive")
        return values


class Aggregation(aggregation_model.Aggregation):
    """Extends Aggregation to allow nullable tag values"""

    tag: str | None = None  # type: ignore[assignment]

class CostReportSettings(settings_model.Settings):
    """Extends Settings to allow nullable fields for report settings"""

    include_credits: bool | None = None  # type: ignore[assignment]
    include_refunds: bool | None = None  # type: ignore[assignment]
    include_discounts: bool | None = None  # type: ignore[assignment]
    include_tax: bool | None = None  # type: ignore[assignment]
    amortize: bool | None = None  # type: ignore[assignment]
    unallocated: bool | None = None  # type: ignore[assignment]
    aggregate_by: str | None = None  # type: ignore[assignment]
    show_previous_period: bool | None = None  # type: ignore[assignment]


class CostReport(cost_report_model.CostReport):
    """Extends CostReport to make chart_settings optional"""

    chart_settings: chart_settings_model.ChartSettings | None = None  # type: ignore[assignment]
    settings: CostReportSettings | None = None  # type: ignore[assignment]


class CostReports(cost_reports_model.CostReports):
    """Extends CostReports to use the custom CostReport model"""

    cost_reports: Sequence[CostReport]  # type: ignore[assignment]


class BudgetAlert(budget_alert_model.BudgetAlert):
    """Extends BudgetAlert to match API response types"""

    threshold: int | None = None  # type: ignore[assignment]
    duration_in_days: int | None = None  # type: ignore[assignment]
    recipient_channels: Sequence[str] | None = None  # type: ignore[assignment]


class BudgetAlerts(budget_alerts_model.BudgetAlerts):
    """Extends BudgetAlerts to use the custom BudgetAlert model"""

    budget_alerts: Sequence[BudgetAlert]  # type: ignore[assignment]


class Me(me_model.Me):
    """Extends Me to handle nullable default workspace tokens"""

    default_workspace_token: str | None = None  # type: ignore[assignment]


class BusinessMetric(business_metric_model.BusinessMetric):
    """Extends BusinessMetric to handle missing import_type values"""

    import_type: str | None = None  # type: ignore[assignment]

class BusinessMetrics(business_metrics_model.BusinessMetrics):
    """Extends BusinessMetrics to use the custom BusinessMetric model"""

    business_metrics: Sequence[BusinessMetric]  # type: ignore[assignment]


class BudgetPeriod(budget_period_model.BudgetPeriod):
    """Extends BudgetPeriod to allow missing end dates"""

    end_at: str | None = None  # type: ignore[assignment]


class Budget(budget_model.Budget):
    """Extends Budget to use the custom BudgetPeriod model"""

    periods: Sequence[BudgetPeriod]  # type: ignore[assignment]


class Budgets(budgets_model.Budgets):
    """Extends Budgets to use the custom Budget model"""

    budgets: Sequence[Budget]  # type: ignore[assignment]


class AnomalyNotification(anomaly_notification_model.AnomalyNotification):
    """Extends AnomalyNotification to allow empty recipients"""

    user_tokens: Sequence[str] | None = None  # type: ignore[assignment]
    recipient_channels: Sequence[str] | None = None  # type: ignore[assignment]
    threshold: int | None = None  # type: ignore[assignment]


class AnomalyNotifications(anomaly_notifications_model.AnomalyNotifications):
    """Extends AnomalyNotifications to use the custom AnomalyNotification model"""

    anomaly_notifications: Sequence[AnomalyNotification]  # type: ignore[assignment]


# --------------------------------
# Model Extensions
# --------------------------------

class RecommendationResource(provider_resource_model.ProviderResource):
    """Alias for ProviderResource model"""

class RecommendationResources(recommendation_provider_resources_model.RecommendationProviderResources):
    """Alias for RecommendationProviderResources model"""


class Recommendation(recommendation_model.Recommendation):
    """Extends Recommendation to handle mismatched field types"""

    resources_affected_count: int | None = Field(default=None)  # type: ignore[assignment]


class Recommendations(recommendations_model.Recommendations):
    """Extends Recommendations to use the custom Recommendation model"""

    recommendations: Sequence[Recommendation]  # type: ignore[assignment]
