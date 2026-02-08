import time

import pytest

from tests.conftest import RESOURCES, settings
from vantage_sdk.models import (
    UpdateAccessGrantAccess,
    AccessGrantTokenParams,
    AnomalyAlertsGetParametersQuery,
    AnomalyNotificationTokenParams,
    AuditLog,
    AuditLogs,
    AuditLogsGetParametersQuery,
    AuditLogTokenParams,
    BillingRuleTokenParams,
    BudgetAlertsBudgetAlertTokenPutRequest,
    BudgetAlertTokenParams,
    BudgetsBudgetTokenGetParametersQuery,
    BudgetTokenParams,
    BusinessMetricsBusinessMetricTokenValuesGetParametersQuery,
    BusinessMetricTokenParams,
    BusinessMetricValues,
    UpdateCostReportChartSettings,
    UpdateCostReportChartType,
    CostAlertsCostAlertTokenEventsGetParametersQuery,
    CostAlertTokenParams,
    CostReportTokenParams,
    CreateBusinessMetric,
    CreateUserFeedback,
    DashboardTokenParams,
    DataExport,
    DataExportTokenParams,
    UpdateCostReportDateBin,
    CreateUnitCostsExportDateBin,
    UpdateCostReportDateInterval,
    FinancialCommitmentReportTokenParams,
    FolderTokenParams,
    KubernetesEfficiencyReportTokenParams,
    ManagedAccountTokenParams,
    NetworkFlowReportTokenParams,

    ProductIdParams,
    ProductPriceIdParams,
    ResourceReportTokenParams,
    ResourcesGetParametersQuery,
    ResourceTokenParams,
    SavedFilterTokenParams,
    UpdateCostReportSettings,
    TeamTokenParams,
    UnitCostsDataExportsPostRequest,
    UnitCostsGetParametersQuery,
    UpdateAccessGrant,
    UpdateAnomalyNotification,
    UpdateBillingRule,
    UpdateBudget,
    UpdateCostAlert,
    UpdateCostReport,
    UpdateDashboard,
    UpdateFinancialCommitmentReport,
    UpdateFolder,
    UpdateKubernetesEfficiencyReport,
    UpdateManagedAccount,
    UpdateNetworkFlowReport,
    UpdateResourceReport,
    UpdateTag,
    UpdateTeam,
    UpdateVirtualTagConfig,
    UpdateVirtualTagConfigValue,
    VirtualTagTokenParams,
    WorkspacesWorkspaceTokenPutRequest,
    WorkspaceTokenParams,
)


def test_get_folder(vantage_sdk, folder_fixture):
    params = FolderTokenParams(folder_token=folder_fixture.token)
    folder_fixture_var = vantage_sdk.get_folder(params)
    assert folder_fixture_var is not None
    assert folder_fixture_var.title == folder_fixture.title


def test_get_all_folders(vantage_sdk):
    folders = vantage_sdk.get_all_folders()
    assert folders is not None
    assert folders.folders is not None


def test_update_folder(vantage_sdk, folder_fixture):
    updated_title = f"{RESOURCES.updated_prefix}_{folder_fixture.title}"
    folder_update = UpdateFolder(title=updated_title)
    params = FolderTokenParams(folder_token=folder_fixture.token)
    updated_folder = vantage_sdk.update_folder(params, folder_update)

    assert updated_folder is not None
    assert updated_folder.title == updated_title


def test_get_cost_report(vantage_sdk, cost_report_fixture):
    params = CostReportTokenParams(cost_report_token=cost_report_fixture.token)
    cost_report = vantage_sdk.get_cost_report(params)
    assert cost_report is not None
    assert cost_report.title == cost_report_fixture.title


def test_get_all_cost_reports(vantage_sdk):
    cost_reports = vantage_sdk.get_all_cost_reports()
    assert len(cost_reports.cost_reports) > 0
    report = cost_reports.cost_reports[0]
    assert report.token is not None
    assert report.title is not None


@pytest.mark.slow
def test_get_data_export(vantage_sdk, create_data_export, cost_report_fixture):
    params = DataExportTokenParams(data_export_token=create_data_export)

    timeout_limit = 100
    timeout_counter = 0
    data_export = None
    success = False

    while timeout_counter < timeout_limit:
        data_export = vantage_sdk.get_data_export(params)
        print(f"Attempt {timeout_counter + 1}")
        match data_export:
            case int():
                timeout_counter += 1
                time.sleep(data_export)
            case DataExport() if data_export.status.lower() == "completed":
                success = True
                break
            case DataExport() if data_export.status.lower() == "failed":
                pytest.fail("Data export failed")
            case _:
                pytest.fail("Something went wrong")

    if not success:
        pytest.fail("Data export timed out")

    assert data_export.manifest.completed_at is not None


def test_update_cost_report(vantage_sdk, cost_report_fixture):
    updated_title = f"{RESOURCES.updated_prefix}_{cost_report_fixture.title}"
    cost_report_update = UpdateCostReport(
        title=updated_title,
        groupings="provider,service",
        filter="costs.provider = 'aws'",
        saved_filter_tokens=None,
        business_metric_tokens_with_metadata=None,
        folder_token=None,
        settings=UpdateCostReportSettings(
            include_credits=True,
            include_refunds=True,
            include_discounts=True,
            include_tax=True,
            amortize=True,
            unallocated=False,
            aggregate_by="cost",
            show_previous_period=True,
        ),
        chart_settings=UpdateCostReportChartSettings(
            x_axis_dimension=["date"],
            y_axis_dimension="cost",
        ),
        date_interval=UpdateCostReportDateInterval.last_3_months,
        chart_type=UpdateCostReportChartType.line,
        date_bin=UpdateCostReportDateBin.month,
    )
    params = CostReportTokenParams(cost_report_token=cost_report_fixture.token)
    updated_cost_report = vantage_sdk.update_cost_report(params, cost_report_update)

    assert updated_cost_report is not None
    assert updated_cost_report.title == updated_title


def test_get_saved_filter(vantage_sdk, saved_filter_fixture):
    params = SavedFilterTokenParams(saved_filter_token=saved_filter_fixture.token)
    saved_filter = vantage_sdk.get_saved_filter(params)
    assert saved_filter is not None
    assert saved_filter.title == saved_filter_fixture.title


def test_get_all_saved_filters(vantage_sdk):
    saved_filters = vantage_sdk.get_all_saved_filters()
    assert saved_filters is not None
    if saved_filters.saved_filters:
        saved_filter = saved_filters.saved_filters[0]
        assert saved_filter.token is not None
        assert saved_filter.title is not None


def test_get_virtual_tag(vantage_sdk, virtual_tag_fixture):
    params = VirtualTagTokenParams(virtual_tag_token=virtual_tag_fixture.token)
    virtual_tag = vantage_sdk.get_virtual_tag(params)
    assert virtual_tag is not None
    assert virtual_tag.key == virtual_tag_fixture.key


def test_update_virtual_tag(vantage_sdk, virtual_tag_fixture):
    updated_key = f"{RESOURCES.updated_prefix}_{virtual_tag_fixture.key}"
    new_value_name = f"{RESOURCES.updated_prefix}_virtual_tag_value"

    new_value = UpdateVirtualTagConfigValue(
        filter="costs.provider = 'aws' AND costs.service = 'Amazon Simple Storage Service'",
        name=new_value_name,
    )

    virtual_tag_update_params = UpdateVirtualTagConfig(key=updated_key, values=[new_value])

    virtual_tag_token_params = VirtualTagTokenParams(virtual_tag_token=virtual_tag_fixture.token)

    updated_virtual_tag = vantage_sdk.update_virtual_tag(virtual_tag_token_params, virtual_tag_update_params)

    assert updated_virtual_tag is not None
    assert updated_virtual_tag.key == updated_key

    value_names = [value.name for value in updated_virtual_tag.values]
    assert new_value_name in value_names


def test_get_all_virtual_tags(vantage_sdk, virtual_tag_fixture):
    virtual_tags = vantage_sdk.get_all_virtual_tags()
    assert virtual_tags is not None
    assert virtual_tag_fixture.token in [vt.token for vt in virtual_tags.virtual_tag_configs]
    first_tag = virtual_tags.virtual_tag_configs[0]
    assert first_tag.token is not None
    assert first_tag.key is not None


def test_get_all_business_metrics(vantage_sdk, business_metric_fixture):
    business_metrics = vantage_sdk.get_all_business_metrics()
    assert len(business_metrics.business_metrics) > 0
    assert business_metric_fixture.token in [bm.token for bm in business_metrics.business_metrics]
    metric = business_metrics.business_metrics[0]
    assert metric.token is not None
    assert metric.title is not None


def test_get_business_metric(business_metric_fixture, vantage_sdk):
    business_metric_token = business_metric_fixture.token
    params = BusinessMetricTokenParams(business_metric_token=business_metric_token)
    business_metric = vantage_sdk.get_business_metric(params)
    assert business_metric is not None
    assert business_metric.token == business_metric_fixture.token
    assert business_metric.title == business_metric_fixture.title


def test_update_business_metric(vantage_sdk, business_metric_fixture):
    updated_title = f"{RESOURCES.updated_prefix}_{business_metric_fixture.title}"
    business_metric_update = CreateBusinessMetric(title=updated_title)
    params = BusinessMetricTokenParams(business_metric_token=business_metric_fixture.token)
    updated_business_metric = vantage_sdk.update_business_metric(params, business_metric_update)

    assert updated_business_metric is not None
    assert updated_business_metric.title == updated_title


def test_get_business_metric_values(vantage_sdk, business_metric_fixture):
    business_metric_token = business_metric_fixture.token
    params = BusinessMetricsBusinessMetricTokenValuesGetParametersQuery(limit=1)
    business_metric_token_params = BusinessMetricTokenParams(business_metric_token=business_metric_token)
    business_metric_values: BusinessMetricValues = vantage_sdk.get_business_metric_values(
        params, business_metric_token_params
    )

    # This can't truly be tested unless a csv file is uploaded to the business metric, for now we just check if the object has the expected attribute
    assert hasattr(business_metric_values, "values")


# ---- Access Grants Tests ----


@pytest.mark.skip(reason="Sandbox account does not have team permissions")
def test_get_all_access_grants(vantage_sdk):
    access_grants = vantage_sdk.get_all_access_grants()
    assert access_grants is not None
    if access_grants.access_grants:
        access_grant = access_grants.access_grants[0]
        assert access_grant.token is not None
        assert access_grant.access is not None


@pytest.mark.skip(reason="Sandbox account does not have team permissions")
def test_get_access_grant(vantage_sdk, access_grant_fixture):
    params = AccessGrantTokenParams(access_grant_token=access_grant_fixture.token)
    access_grant = vantage_sdk.get_access_grant(params)
    assert access_grant is not None
    assert access_grant.token == access_grant_fixture.token


@pytest.mark.skip(reason="Sandbox account does not have team permissions")
def test_access_grant_with_denied_access(vantage_sdk, access_grant_denied_fixture):
    access_grant = access_grant_denied_fixture

    assert access_grant is not None
    assert access_grant.access == "denied"
    assert access_grant.token.startswith("rsrc_accss_grnt_")


@pytest.mark.skip(reason="Sandbox account does not have team permissions")
def test_update_access_grant(vantage_sdk, access_grant_fixture):
    params = AccessGrantTokenParams(access_grant_token=access_grant_fixture.token)

    # Change access from allowed to denied
    access_grant_update = UpdateAccessGrant(access=UpdateAccessGrantAccess.denied)
    updated_access_grant = vantage_sdk.update_access_grant(params, access_grant_update)

    assert updated_access_grant is not None
    assert updated_access_grant.access == "denied"

    # Change back to allowed
    access_grant_update = UpdateAccessGrant(access=UpdateAccessGrantAccess.allowed)
    updated_access_grant = vantage_sdk.update_access_grant(params, access_grant_update)

    assert updated_access_grant is not None
    assert updated_access_grant.access == "allowed"


# ---- Teams Tests ----


@pytest.mark.skip(reason="Sandbox account does not have team permissions")
def test_get_all_teams(vantage_sdk):
    """There is always at least one team in a Vantage account"""
    teams = vantage_sdk.get_all_teams()
    assert teams is not None
    assert len(teams.teams) > 0
    team = teams.teams[0]
    assert team.token is not None
    assert team.name is not None


@pytest.mark.skip(reason="Sandbox account does not have team permissions")
def test_get_team(vantage_sdk, team_fixture):
    params = TeamTokenParams(team_token=team_fixture.token)
    team = vantage_sdk.get_team(params)
    assert team is not None
    assert team.token == team_fixture.token


@pytest.mark.skip(reason="Sandbox account does not have team permissions")
def test_update_team(vantage_sdk, team_fixture):
    params = TeamTokenParams(team_token=team_fixture.token)

    updated_name = f"{RESOURCES.updated_prefix}_{team_fixture.name}"
    team_update = UpdateTeam(name=updated_name, description="Updated description")
    updated_team = vantage_sdk.update_team(params, team_update)

    assert updated_team is not None
    assert updated_team.name == updated_name


# ---- Me API Tests ----

def test_get_me(vantage_sdk):
    me_info = vantage_sdk.get_me()
    assert me_info is not None

# ---- Anomaly Alerts & Notifications Tests ----


@pytest.mark.skip(reason="Anomaly alerts request exceeded 60s timeout")
def test_get_all_anomaly_alerts(vantage_sdk):
    # Test with parameters to avoid timeout
    params = AnomalyAlertsGetParametersQuery(limit=10)


def test_get_all_anomaly_notifications(vantage_sdk):
    anomaly_notifications = vantage_sdk.get_all_anomaly_notifications()
    assert anomaly_notifications is not None
    if anomaly_notifications.anomaly_notifications:
        notification = anomaly_notifications.anomaly_notifications[0]
        assert notification.token is not None
        assert notification.cost_report_token is not None


def test_get_anomaly_notification(vantage_sdk, anomaly_notification_fixture):
    params = AnomalyNotificationTokenParams(anomaly_notification_token=anomaly_notification_fixture.token)
    anomaly_notification = vantage_sdk.get_anomaly_notification(params)
    assert anomaly_notification is not None
    assert anomaly_notification.token == anomaly_notification_fixture.token


def test_anomaly_notification_with_different_threshold(vantage_sdk, anomaly_notification_threshold_2000_fixture):
    anomaly_notification = anomaly_notification_threshold_2000_fixture

    assert anomaly_notification is not None
    assert anomaly_notification.threshold == 2000
    assert anomaly_notification.token.startswith("rprt_alrt_")


def test_update_anomaly_notification(vantage_sdk, anomaly_notification_fixture):
    params = AnomalyNotificationTokenParams(anomaly_notification_token=anomaly_notification_fixture.token)

    # Update the notification threshold
    notification_update = UpdateAnomalyNotification(threshold=3000)
    updated_notification = vantage_sdk.update_anomaly_notification(params, notification_update)

    assert updated_notification is not None
    assert updated_notification.threshold == 3000

    # Update back to original
    notification_update = UpdateAnomalyNotification(threshold=1000)
    updated_notification = vantage_sdk.update_anomaly_notification(params, notification_update)

    assert updated_notification is not None
    assert updated_notification.threshold == 1000


# ---- Billing Rules Tests ----


@pytest.mark.skip(reason="Billing rules require enterprise permissions")
def test_get_all_billing_rules(vantage_sdk):
    billing_rules = vantage_sdk.get_all_billing_rules()
    assert billing_rules is not None


@pytest.mark.skip(reason="Billing rules require enterprise permissions")
def test_get_billing_rule(vantage_sdk, billing_rule_fixture):
    params = BillingRuleTokenParams(billing_rule_token=billing_rule_fixture.token)
    billing_rule = vantage_sdk.get_billing_rule(params)
    assert billing_rule is not None
    assert billing_rule.token == billing_rule_fixture.token


@pytest.mark.skip(reason="Billing rules require enterprise permissions")
def test_update_billing_rule(vantage_sdk, billing_rule_fixture):
    params = BillingRuleTokenParams(billing_rule_token=billing_rule_fixture.token)

    updated_title = f"{RESOURCES.updated_prefix}_{billing_rule_fixture.title}"
    billing_rule_update = UpdateBillingRule(title=updated_title)
    updated_rule = vantage_sdk.update_billing_rule(params, billing_rule_update)

    assert updated_rule is not None
    assert updated_rule.title == updated_title


# ---- Cost Providers & Services Tests ----


def test_get_cost_providers(vantage_sdk):
    workspace_token_params = WorkspaceTokenParams(workspace_token=settings.workspace_token)
    cost_providers = vantage_sdk.get_cost_providers(workspace_token_params)
    assert cost_providers is not None
    assert cost_providers.cost_providers is not None


def test_get_cost_services(vantage_sdk):
    workspace_token_params = WorkspaceTokenParams(workspace_token=settings.workspace_token)
    cost_services = vantage_sdk.get_cost_services(workspace_token_params)
    assert cost_services is not None
    assert cost_services.cost_services is not None


# ---- Budgets Tests ----


def test_get_all_budgets(vantage_sdk):
    budgets = vantage_sdk.get_all_budgets()
    assert budgets is not None
    if budgets.budgets:
        budget = budgets.budgets[0]
        assert budget.token is not None
        assert budget.name is not None


def test_get_budget(vantage_sdk, budget_fixture):
    params = BudgetTokenParams(budget_token=budget_fixture.token)
    budget = vantage_sdk.get_budget(params)
    assert budget is not None
    assert budget.token == budget_fixture.token


def test_get_budget_with_params(vantage_sdk, budget_fixture):
    params = BudgetTokenParams(budget_token=budget_fixture.token)
    query_params = BudgetsBudgetTokenGetParametersQuery(include_budget_alert_cost_data=True)
    budget = vantage_sdk.get_budget(params, query_params)
    assert budget is not None
    assert budget.token == budget_fixture.token


def test_update_budget(vantage_sdk, budget_fixture):
    params = BudgetTokenParams(budget_token=budget_fixture.token)

    updated_name = f"{RESOURCES.updated_prefix}_{budget_fixture.name}"
    budget_update = UpdateBudget(
        name=updated_name,
    )
    updated_budget = vantage_sdk.update_budget(params, budget_update)

    assert updated_budget is not None
    assert updated_budget.name == updated_name


# ---- Budget Alerts Tests ----


def test_get_all_budget_alerts(vantage_sdk):
    budget_alerts = vantage_sdk.get_all_budget_alerts()
    assert budget_alerts is not None
    if budget_alerts.budget_alerts:
        alert = budget_alerts.budget_alerts[0]
        assert alert.token is not None
        assert alert.budget_tokens is not None


def test_get_budget_alert(vantage_sdk, budget_alert_fixture):
    params = BudgetAlertTokenParams(budget_alert_token=budget_alert_fixture.token)
    budget_alert = vantage_sdk.get_budget_alert(params)
    assert budget_alert is not None
    assert budget_alert.token == budget_alert_fixture.token


@pytest.mark.skip(reason="Budget alert updates require workspace and user token configuration not available in test environment")
def test_update_budget_alert(vantage_sdk, budget_alert_fixture):
    params = BudgetAlertTokenParams(budget_alert_token=budget_alert_fixture.token)

    # Update the budget alert threshold
    budget_alert_update = BudgetAlertsBudgetAlertTokenPutRequest(
        threshold=80  # Alert at 80% of budget
    )
    updated_budget_alert = vantage_sdk.update_budget_alert(params, budget_alert_update)

    assert updated_budget_alert is not None
    assert updated_budget_alert.threshold == 80

    # Update back to original
    budget_alert_update = BudgetAlertsBudgetAlertTokenPutRequest(threshold=50)
    updated_budget_alert = vantage_sdk.update_budget_alert(params, budget_alert_update)

    assert updated_budget_alert is not None
    assert updated_budget_alert.threshold == 50


# ---- Cost Alerts Tests ----


def test_get_all_cost_alerts(vantage_sdk):
    cost_alerts = vantage_sdk.get_all_cost_alerts()
    assert cost_alerts is not None
    if cost_alerts.cost_alerts:
        alert = cost_alerts.cost_alerts[0]
        assert alert.token is not None
        assert alert.title is not None


@pytest.mark.skip(reason="Cost alerts require email recipients belonging to org users or a connected Slack integration")
def test_get_cost_alert(vantage_sdk, cost_alert_fixture):
    params = CostAlertTokenParams(cost_alert_token=cost_alert_fixture.token)
    cost_alert = vantage_sdk.get_cost_alert(params)
    assert cost_alert is not None
    assert cost_alert.token == cost_alert_fixture.token


@pytest.mark.skip(reason="Cost alerts require email recipients belonging to org users or a connected Slack integration")
def test_get_cost_alert_events(vantage_sdk, cost_alert_fixture):
    params = CostAlertTokenParams(cost_alert_token=cost_alert_fixture.token)

    # Get events without query params
    events = vantage_sdk.get_cost_alert_events(params)
    assert events is not None
    if events.events:
        event = events.events[0]
        assert event.token is not None
        assert event.cost_alert_token is not None

    # Get events with query params

    query_params = CostAlertsCostAlertTokenEventsGetParametersQuery(limit=10)
    events = vantage_sdk.get_cost_alert_events(params, query_params)
    assert events is not None


@pytest.mark.skip(reason="Cost alerts require email recipients belonging to org users or a connected Slack integration")
def test_update_cost_alert(vantage_sdk, cost_alert_fixture):
    params = CostAlertTokenParams(cost_alert_token=cost_alert_fixture.token)

    updated_title = f"{RESOURCES.updated_prefix}_{cost_alert_fixture.title}"
    cost_alert_update = UpdateCostAlert(
        threshold=5000,
        title=updated_title,
    )
    updated_cost_alert = vantage_sdk.update_cost_alert(params, cost_alert_update)

    assert updated_cost_alert is not None
    assert updated_cost_alert.threshold == 5000
    assert updated_cost_alert.title == updated_title


def test_get_all_dashboards(vantage_sdk):
    dashboards = vantage_sdk.get_all_dashboards()
    assert dashboards is not None
    assert hasattr(dashboards, "dashboards")
    if dashboards.dashboards:
        dashboard = dashboards.dashboards[0]
        assert dashboard.token is not None
        assert dashboard.title is not None


def test_get_dashboard(vantage_sdk, dashboard_fixture):
    params = DashboardTokenParams(dashboard_token=dashboard_fixture.token)
    dashboard = vantage_sdk.get_dashboard(params)
    assert dashboard is not None
    assert dashboard.token == dashboard_fixture.token


def test_update_dashboard(vantage_sdk, dashboard_fixture):
    params = DashboardTokenParams(dashboard_token=dashboard_fixture.token)
    updated_title = f"{RESOURCES.updated_prefix}_{dashboard_fixture.title}"

    # Simple update - just change the title
    dashboard_update = UpdateDashboard(
        title=updated_title,
        workspace_token=dashboard_fixture.workspace_token,  # Include workspace token
    )

    updated_dashboard = vantage_sdk.update_dashboard(params, dashboard_update)
    assert updated_dashboard is not None
    assert updated_dashboard.title == updated_title


# ---- Financial Commitments & Reports Tests ----


def test_get_all_financial_commitments(vantage_sdk):
    financial_commitments = vantage_sdk.get_all_financial_commitments()
    assert financial_commitments is not None
    assert financial_commitments.financial_commitments is not None


def test_get_all_financial_commitment_reports(vantage_sdk):
    financial_commitment_reports = vantage_sdk.get_all_financial_commitment_reports()
    assert financial_commitment_reports is not None
    if financial_commitment_reports.financial_commitment_reports:
        report = financial_commitment_reports.financial_commitment_reports[0]
        assert report.token is not None
        assert report.title is not None


def test_get_financial_commitment_report(vantage_sdk, financial_commitment_report_fixture):
    params = FinancialCommitmentReportTokenParams(
        financial_commitment_report_token=financial_commitment_report_fixture.token
    )
    financial_commitment_report = vantage_sdk.get_financial_commitment_report(params)
    assert financial_commitment_report is not None
    assert financial_commitment_report.title == financial_commitment_report_fixture.title


def test_update_financial_commitment_report(vantage_sdk, financial_commitment_report_fixture):
    updated_title = f"{RESOURCES.updated_prefix}_{financial_commitment_report_fixture.title}"
    report_update = UpdateFinancialCommitmentReport(title=updated_title)
    params = FinancialCommitmentReportTokenParams(
        financial_commitment_report_token=financial_commitment_report_fixture.token
    )
    updated = vantage_sdk.update_financial_commitment_report(params, report_update)

    assert updated is not None
    assert updated.title == updated_title


# ---- Kubernetes Efficiency Reports Tests ----


def test_get_all_kubernetes_efficiency_reports(vantage_sdk):
    kubernetes_efficiency_reports = vantage_sdk.get_all_kubernetes_efficiency_reports()
    assert kubernetes_efficiency_reports is not None
    if kubernetes_efficiency_reports.kubernetes_efficiency_reports:
        report = kubernetes_efficiency_reports.kubernetes_efficiency_reports[0]
        assert report.token is not None
        assert report.title is not None


def test_get_kubernetes_efficiency_report(vantage_sdk, kubernetes_efficiency_report_fixture):
    params = KubernetesEfficiencyReportTokenParams(
        kubernetes_efficiency_report_token=kubernetes_efficiency_report_fixture.token
    )
    kubernetes_efficiency_report = vantage_sdk.get_kubernetes_efficiency_report(params)
    assert kubernetes_efficiency_report is not None
    assert kubernetes_efficiency_report.title == kubernetes_efficiency_report_fixture.title


def test_update_kubernetes_efficiency_report(vantage_sdk, kubernetes_efficiency_report_fixture):
    updated_title = f"{RESOURCES.updated_prefix}_{kubernetes_efficiency_report_fixture.title}"
    report_update = UpdateKubernetesEfficiencyReport(title=updated_title)
    params = KubernetesEfficiencyReportTokenParams(
        kubernetes_efficiency_report_token=kubernetes_efficiency_report_fixture.token
    )
    updated = vantage_sdk.update_kubernetes_efficiency_report(params, report_update)

    assert updated is not None
    assert updated.title == updated_title


# ---- Managed Accounts Tests ----


@pytest.mark.skip(reason="Managed accounts require enterprise permissions")
def test_get_all_managed_accounts(vantage_sdk):
    managed_accounts = vantage_sdk.get_all_managed_accounts()
    assert managed_accounts is not None


@pytest.mark.skip(reason="Managed accounts require enterprise permissions")
def test_get_managed_account(vantage_sdk, managed_account_fixture):
    params = ManagedAccountTokenParams(managed_account_token=managed_account_fixture.token)
    managed_account = vantage_sdk.get_managed_account(params)
    assert managed_account is not None
    assert managed_account.token == managed_account_fixture.token
    assert managed_account.name == managed_account_fixture.name
    assert managed_account.contact_email == managed_account_fixture.contact_email


@pytest.mark.skip(reason="Managed accounts require enterprise permissions")
def test_update_managed_account(vantage_sdk, managed_account_fixture):
    updated_name = f"{RESOURCES.updated_prefix}_{managed_account_fixture.name}"
    updated_email = "updated@example.com"
    account_update = UpdateManagedAccount(name=updated_name, contact_email=updated_email)
    params = ManagedAccountTokenParams(managed_account_token=managed_account_fixture.token)
    updated = vantage_sdk.update_managed_account(params, account_update)

    assert updated is not None
    assert updated.name == updated_name
    assert updated.contact_email == updated_email


# ---- Network Flow Reports Tests ----


def test_get_all_network_flow_reports(vantage_sdk):
    network_flow_reports = vantage_sdk.get_all_network_flow_reports()
    assert network_flow_reports is not None
    if network_flow_reports.network_flow_reports:
        report = network_flow_reports.network_flow_reports[0]
        assert report.token is not None
        assert report.title is not None


def test_get_network_flow_report(vantage_sdk, network_flow_report_fixture):
    params = NetworkFlowReportTokenParams(network_flow_report_token=network_flow_report_fixture.token)
    network_flow_report = vantage_sdk.get_network_flow_report(params)
    assert network_flow_report is not None
    assert network_flow_report.title == network_flow_report_fixture.title


def test_update_network_flow_report(vantage_sdk, network_flow_report_fixture):
    updated_title = f"{RESOURCES.updated_prefix}_{network_flow_report_fixture.title}"
    report_update = UpdateNetworkFlowReport(title=updated_title)
    params = NetworkFlowReportTokenParams(network_flow_report_token=network_flow_report_fixture.token)
    updated = vantage_sdk.update_network_flow_report(params, report_update)

    assert updated is not None
    assert updated.title == updated_title


# ---- Products & Pricing Tests ----


def test_get_all_products(vantage_sdk):
    products = vantage_sdk.get_all_products()
    assert products is not None
    # We expect at least one product in any Vantage account
    assert len(products.products) > 0


def test_get_product(vantage_sdk):
    # First get all products to get a valid product ID
    products = vantage_sdk.get_all_products()
    assert products is not None
    assert len(products.products) > 0

    # Get the first product ID
    product_id = products.products[0].id

    # Get the specific product
    params = ProductIdParams(id=product_id)
    product = vantage_sdk.get_product(params)

    assert product is not None
    assert product.id == product_id


def test_get_product_prices(vantage_sdk):
    # First get all products to get a valid product ID
    products = vantage_sdk.get_all_products()
    assert products is not None
    assert len(products.products) > 0

    # Get the first product ID
    product_id = products.products[0].id

    # Get prices for the product
    params = ProductIdParams(id=product_id)
    prices = vantage_sdk.get_product_prices(params)

    assert prices is not None
    if prices.prices:
        price = prices.prices[0]
        assert price.id is not None


def test_get_product_price(vantage_sdk):
    # First get all products to get a valid product ID
    products = vantage_sdk.get_all_products()
    assert products is not None
    assert len(products.products) > 0

    # Get the first product ID
    product_id = products.products[0].id

    # Get prices for the product
    product_params = ProductIdParams(id=product_id)
    prices = vantage_sdk.get_product_prices(product_params)

    # If there are prices, test getting a specific price
    if prices is not None and len(prices.prices) > 0:
        price_id = prices.prices[0].id

        price_params = ProductPriceIdParams(id=price_id)
        price = vantage_sdk.get_product_price(product_params, price_params)

        assert price is not None
        assert price.id == price_id


# ---- Recommendations Tests ----


def test_get_all_recommendations(vantage_sdk):
    recommendations = vantage_sdk.get_all_recommendations()
    assert recommendations is not None
    if recommendations.recommendations:
        recommendation = recommendations.recommendations[0]
        assert recommendation.token is not None
        assert recommendation.description is not None


def test_get_recommendation_and_resources():
    # This test simply checks that the methods are available and don't raise errors
    # We can't test with actual data without knowing the recommendation tokens
    # which would require a specific account setup
    pass


# ---- Report Notifications Tests ----


def test_get_all_report_notifications(vantage_sdk):
    report_notifications = vantage_sdk.get_all_report_notifications()
    assert report_notifications is not None
    if report_notifications.report_notifications:
        notification = report_notifications.report_notifications[0]
        assert notification.token is not None
        assert notification.cost_report_token is not None


def test_report_notification_methods():
    # This test simply checks that the methods are available and don't raise errors
    # We can't test with actual data without knowing the report notification tokens
    # or having permission to create report notifications
    pass


# ---- Resource Reports Tests ----


def test_get_all_resource_reports(vantage_sdk):
    resource_reports = vantage_sdk.get_all_resource_reports()
    assert resource_reports is not None
    if resource_reports.resource_reports:
        report = resource_reports.resource_reports[0]
        assert report.token is not None
        assert report.title is not None


def test_get_resource_report(vantage_sdk, resource_report_fixture):
    params = ResourceReportTokenParams(resource_report_token=resource_report_fixture.token)
    resource_report = vantage_sdk.get_resource_report(params)
    assert resource_report is not None
    assert resource_report.title == resource_report_fixture.title


def test_update_resource_report(vantage_sdk, resource_report_fixture):
    updated_title = f"{RESOURCES.updated_prefix}_{resource_report_fixture.title}"
    report_update = UpdateResourceReport(title=updated_title)
    params = ResourceReportTokenParams(resource_report_token=resource_report_fixture.token)
    updated = vantage_sdk.update_resource_report(params, report_update)

    assert updated is not None
    assert updated.title == updated_title


# ---- Resources Tests ----


@pytest.mark.skip(reason="Resources endpoints are prone to 504 timeouts in the test environment")
def test_get_all_resources(vantage_sdk, resource_report_fixture):
    query_params = ResourcesGetParametersQuery(resource_report_token=resource_report_fixture.token, limit=25)
    resources = vantage_sdk.get_all_resources(query_params)
    if not resources.resources:
        resource_report_tokens = [report.token for report in vantage_sdk.get_all_resource_reports().resource_reports]
        for token in resource_report_tokens:
            fallback_query = ResourcesGetParametersQuery(resource_report_token=token, limit=25)
            resources = vantage_sdk.get_all_resources(fallback_query)
            if resources.resources:
                break

    if not resources.resources:
        pytest.skip("No resources found for resource reports in test environment")

    resource = resources.resources[0]
    assert resource.token is not None
    assert resource.uuid is not None


@pytest.mark.skip(reason="Resources endpoints are prone to 504 timeouts in the test environment")
def test_get_resource(vantage_sdk, resource_report_fixture):
    query_params = ResourcesGetParametersQuery(resource_report_token=resource_report_fixture.token, limit=25)
    resources = vantage_sdk.get_all_resources(query_params)

    if not resources.resources:
        resource_report_tokens = [report.token for report in vantage_sdk.get_all_resource_reports().resource_reports]
        for token in resource_report_tokens:
            fallback_query = ResourcesGetParametersQuery(resource_report_token=token, limit=25)
            resources = vantage_sdk.get_all_resources(fallback_query)
            if resources.resources:
                break

    if not resources.resources:
        pytest.skip("No resources found for resource reports in test environment")

    resource_token = resources.resources[0].token
    params = ResourceTokenParams(resource_token=resource_token)
    resource = vantage_sdk.get_resource(params)
    assert resource is not None
    assert resource.token == resource_token


# ---- Tags Tests ----


def test_get_all_tags(vantage_sdk):
    tags = vantage_sdk.get_all_tags()
    assert tags is not None
    assert hasattr(tags, "tags")


@pytest.mark.skip(reason="Sandbox account does not have tags configured")
def test_get_tag_values(vantage_sdk, virtual_tag_fixture):
    # Get all tags - virtual_tag_fixture ensures there's at least one virtual tag in the system
    tags = vantage_sdk.get_all_tags()

    # There should be at least one tag
    assert tags is not None
    assert len(tags.tags) > 0


@pytest.mark.skip(reason="Sandbox account does not have tags configured")
def test_update_tags(vantage_sdk, virtual_tag_fixture):
    tags = vantage_sdk.get_all_tags()
    assert len(tags.tags) > 0

    tag = tags.tags[0]
    tag_key = tag.tag_key
    current_hidden = tag.hidden

    tag_update = UpdateTag(tag_key=tag_key, hidden=not current_hidden)

    updated_tags = vantage_sdk.update_tags(tag_update)
    assert updated_tags is not None
    updated_tag = next(t for t in updated_tags.tags if t.tag_key == tag_key)
    assert updated_tag.hidden == (not current_hidden)

    tag_update = UpdateTag(tag_key=tag_key, hidden=current_hidden)
    vantage_sdk.update_tags(tag_update)


# ---- Unit Costs Tests ----


def test_get_all_unit_costs(vantage_sdk, cost_report_fixture):
    # Test getting all unit costs
    # The cost_report_token is required for this API call
    query_params = UnitCostsGetParametersQuery(cost_report_token=cost_report_fixture.token)
    unit_costs = vantage_sdk.get_all_unit_costs(query_params)

    # Check that the response has the expected structure
    assert unit_costs is not None
    assert unit_costs.unit_costs is not None


@pytest.mark.skip(reason="Unit costs data export requires specific data setup")
def test_create_unit_costs_data_export(vantage_sdk, cost_report_fixture):
    export_request = UnitCostsDataExportsPostRequest(
        cost_report_token=cost_report_fixture.token,
        workspace_token=settings.workspace_token,
        date_bin=CreateUnitCostsExportDateBin.day,
        start_date="2023-01-01",
        end_date="2023-01-31",
    )

    token = vantage_sdk.create_unit_costs_data_export(export_request)
    assert token is not None
    assert isinstance(token, str)


# ---- User Feedback Tests ----


@pytest.mark.skip(reason="User feedback endpoint is disabled in this environment")
def test_create_user_feedback(vantage_sdk):
    # Create test feedback message
    feedback = CreateUserFeedback(message="This is a test feedback message from automated tests. Please ignore.")

    # Submit the feedback
    result = vantage_sdk.create_user_feedback(feedback)

    # Verify the response structure
    assert result is not None
    assert result.message == feedback.message
    assert result.token is not None


# ---- Users APIs Tests ----


def test_get_all_users(vantage_sdk):
    """Test getting all users, there will always be at least one user (the current user)"""
    users = vantage_sdk.get_all_users()
    assert users is not None
    assert len(users.users) > 0
    user = users.users[0]
    assert user.token is not None
    assert user.name is not None


def test_get_user(vantage_sdk):
    """Test getting a specific user

    This test is not possibl to implement becuase you cannot create a user
    via the API, and we do not have access to user tokens in the test environment.
    """
    pass


# ---- Workspaces APIs Tests ----


def test_get_all_workspaces(vantage_sdk):
    """Test getting all workspaces"""
    workspaces = vantage_sdk.get_all_workspaces()
    assert workspaces is not None
    assert len(workspaces.workspaces) > 0
    workspace = workspaces.workspaces[0]
    assert workspace.token is not None
    assert workspace.name is not None


def test_get_workspace(vantage_sdk):
    """Test getting a specific workspace using the workspace token from settings"""
    # Use the workspace token from settings
    params = WorkspaceTokenParams(workspace_token=settings.workspace_token)
    workspace = vantage_sdk.get_workspace(params)

    # Verify the workspace was retrieved correctly
    assert workspace is not None
    assert workspace.token == settings.workspace_token

@pytest.mark.skip(reason="Workspace deletion is not supported in this environment")
def test_update_workspace(vantage_sdk, workspace_fixture):
    """Test updating a workspace's name"""
    updated_name = f"{RESOURCES.updated_prefix}_{workspace_fixture.name}"
    workspace_update = WorkspacesWorkspaceTokenPutRequest(name=updated_name)
    params = WorkspaceTokenParams(workspace_token=workspace_fixture.token)
    updated_workspace = vantage_sdk.update_workspace(params, workspace_update)

    assert updated_workspace is not None
    assert updated_workspace.name == updated_name


# ---- Audit Logs Tests ----
# As of 2025-11-22, Audit logs are available for Virtual Tags, Cost Reports, and FinOps Agents


def test_get_all_audit_logs(vantage_sdk, cost_report_audit_log_fixture):
    """Test getting all audit logs"""
    _, cost_report_token = cost_report_audit_log_fixture

    audit_log_params = AuditLogsGetParametersQuery(object_token=cost_report_token)
    audit_logs: AuditLogs = vantage_sdk.get_all_audit_logs(audit_log_params)

    assert audit_logs.audit_logs is not None
    assert len(audit_logs.audit_logs) > 0

    for log in audit_logs.audit_logs:
        assert log.object_token == cost_report_token


def test_get_audit_log(vantage_sdk, cost_report_audit_log_fixture):
    """Test getting a specific audit log by token"""
    audit_logs_from_fixture, cost_report_token = cost_report_audit_log_fixture

    target_log = audit_logs_from_fixture.audit_logs[0]
    params = AuditLogTokenParams(audit_log_token=target_log.token)
    audit_log: AuditLog = vantage_sdk.get_audit_log(params)

    assert audit_log is not None
    assert audit_log.token == target_log.token
    assert audit_log.object_token == cost_report_token
