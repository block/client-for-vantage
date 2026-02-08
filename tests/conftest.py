"""Test fixtures and VCR configuration for the Vantage SDK integration tests.

Tests run against the live Vantage API by default. When VCR_ENABLED=true,
pytest-recording intercepts HTTP traffic and replays it from YAML cassettes
stored in tests/cassettes/. This lets CI run without network access or API
credentials.

Scrubbing functions (_scrub_request, _scrub_response) strip secrets and
non-deterministic headers before cassettes are written to disk so that
API keys never end up in version control and replayed responses match
regardless of when they were recorded.
"""

from datetime import datetime

# This fixes a type issue with the generated code in models.py
import builtins
import time
from pathlib import Path

builtins.bytes_aliased = bytes

import pytest
from httpx import HTTPError, Timeout

from tests.test_models import Settings, ResourceNameFactory
from vantage_sdk import VantageSDK
from vantage_sdk.models import (
    AccessGrant,
    AccessGrantTokenParams,
    AnomalyNotification,
    AnomalyNotificationTokenParams,
    AuditLog,
    AuditLogs,
    AuditLogsGetParametersQuery,
    BillingRule,
    BillingRuleTokenParams,
    Budget,
    BudgetAlert,
    BudgetAlertTokenParams,
    BudgetAlertsPostRequest,
    BudgetTokenParams,
    BusinessMetric,
    BusinessMetricTokenParams,
    CostAlert,
    CostAlertTokenParams,
    CostReport,
    CostReportTokenParams,
    CostsDataExportsPostRequest,
    CreateCostReportChartType,
    CreateDashboardDateBin,
    CreateCostReportDateBin,
    CreateDashboardDateInterval,
    CreateFinancialCommitmentReportDateInterval,
    CreateKubernetesEfficiencyReportDateInterval,
    CreateNetworkFlowReportDateInterval,
    CreateCostExportSchema,
    CostsGetParametersQuery,
    CreateAccessGrant,
    CreateAccessGrantAccess,
    CreateAnomalyNotification,
    CreateBillingRule,
    CreateBudget,
    CreateBudgetPeriod,
    CreateBusinessMetric,
    CreateBusinessMetricCostReportTokensWithMetadatum,
    CreateBusinessMetricValue,
    CreateCostAlert,
    CreateCostReport,
    CreateDashboard,
    CreateFinancialCommitmentReport,
    CreateFolder,
    CreateKubernetesEfficiencyReport,
    CreateManagedAccount,
    CreateNetworkFlowReport,
    CreateResourceReport,
    CreateSavedFilter,
    CreateTeam,
    CreateTeamRole,
    CreateVirtualTagConfig,
    Dashboard,
    DashboardTokenParams,
    CreateNetworkFlowReportFlowDirection,
    CreateNetworkFlowReportFlowWeight,
    CreateNetworkFlowReportGrouping,
    FinancialCommitmentReport,
    FinancialCommitmentReportTokenParams,
    Folder,
    FolderTokenParams,
    CreateBusinessMetricForecastedValue,
    KubernetesEfficiencyReport,
    KubernetesEfficiencyReportTokenParams,
    CreateCostReportSettings,
    CreateDashboardWidgetSettings,
    CreateVirtualTagConfigValue,
    VirtualTagConfigValue,
    ManagedAccount,
    ManagedAccountTokenParams,
    NetworkFlowReport,
    NetworkFlowReportTokenParams,
    ResourceReport,
    ResourceReportTokenParams,
    SavedFilter,
    SavedFilterTokenParams,
    CreateCostReportChartSettings,
    CreateVirtualTagConfigCollapsedTagKey,
    VirtualTagConfigValueCostMetricAggregation,
    VirtualTagConfigValuePercentage,
    Team,
    TeamTokenParams,
    UpdateCostReport,
    CreateBusinessMetricCostReportTokensWithMetadatumUnitScale,
    CreateDashboardWidget,
    VirtualTagConfig,
    VirtualTagTokenParams,
    CreateWorkspace,
    Workspace,
    WorkspaceTokenParams,
)

RESOURCES = ResourceNameFactory()
CASSETTE_DIR = Path(__file__).parent / "cassettes"

settings = Settings()

def _scrub_request(request):
    if "authorization" in request.headers:
        request.headers["authorization"] = "REDACTED"
    return request

def _scrub_response(response):
    response["headers"].pop("Date", None)
    response["headers"].pop("X-Request-Id", None)
    return response


def pytest_configure(config) -> None:
    """Register custom markers"""
    config.addinivalue_line("markers", "slow: mark test as a long running test")
    config.addinivalue_line("markers", "live: mark test as requiring the live API")

def pytest_collection_modifyitems(items):
    use_vcr = settings.vcr_enabled
    if not use_vcr:
        return
    for item in items:
        item.add_marker(pytest.mark.vcr)

@pytest.fixture(scope="session")
def vcr_config():
    return {
        "cassette_library_dir": str(CASSETTE_DIR),
        "filter_headers": ["authorization"],
        "before_record_request": _scrub_request,
        "before_record_response": _scrub_response,
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "decode_compressed_response": True,
    }


@pytest.fixture()
def vantage_sdk():
    api_key = settings.vantage_api_key
    sdk = VantageSDK(api_key=api_key)
    sdk.timeout = Timeout(300.0, read=None)
    return sdk


@pytest.fixture()
def folder_fixture(vantage_sdk):
    # setup
    folder_title = RESOURCES.folder_name
    new_folder_obj = CreateFolder(
        title=folder_title,
        workspace_token=settings.workspace_token,
        saved_filter_tokens=None,
        parent_folder_token=None,
    )

    folder: Folder = vantage_sdk.create_folder(new_folder=new_folder_obj)
    assert folder is not None
    assert folder.title == folder_title

    yield folder

    # teardown
    params = FolderTokenParams(folder_token=folder.token)
    vantage_sdk.delete_folder(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_folder(params)

    # assert that the folder was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def cost_report_fixture(vantage_sdk):
    # setup
    report_title = RESOURCES.cost_report_name
    new_cost_report = CreateCostReport(
        title=report_title,
        workspace_token=settings.workspace_token,
        date_interval="last_3_months",
        groupings="provider,service",
        filter="costs.provider = 'aws'",
        saved_filter_tokens=None,
        business_metric_tokens_with_metadata=None,
        folder_token=None,
        settings=CreateCostReportSettings(
            include_credits=True,
            include_refunds=True,
            include_discounts=True,
            include_tax=True,
            amortize=True,
            unallocated=False,
            aggregate_by="cost",
            show_previous_period=True,
        ),
        chart_type=CreateCostReportChartType.line,
        date_bin=CreateCostReportDateBin.month,
        chart_settings=CreateCostReportChartSettings(
            x_axis_dimension=["date"],
            y_axis_dimension="cost",
        ),
    )

    cost_report: CostReport = vantage_sdk.create_cost_report(new_cost_report)
    assert cost_report is not None
    assert cost_report.title == report_title

    yield cost_report

    # teardown
    params = CostReportTokenParams(cost_report_token=cost_report.token)
    vantage_sdk.delete_cost_report(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_cost_report(params)

    # assert that the cost report was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def team_fixture(vantage_sdk):
    # setup - create a test team
    test_team_name = RESOURCES.team_name
    new_team = CreateTeam(
        name=test_team_name,
        workspace_tokens=[settings.workspace_token],
        role=CreateTeamRole.viewer,
        description="Test team",
        user_tokens=None,
        user_emails=None,
    )

    team: Team = vantage_sdk.create_team(new_team)
    assert team is not None
    assert team.name == test_team_name

    yield team

    # teardown
    params = TeamTokenParams(team_token=team.token)
    vantage_sdk.delete_team(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_team(params)

    # assert that the team was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def workspace_fixture(vantage_sdk):
    """Fixture to create a workspace for testing"""
    # setup
    workspace_name = RESOURCES.workspace_name
    new_workspace = CreateWorkspace(name=workspace_name)

    workspace: Workspace = vantage_sdk.create_workspace(new_workspace)
    assert workspace is not None
    assert workspace.name == workspace_name
    assert workspace.token is not None

    yield workspace

    # teardown
    params = WorkspaceTokenParams(workspace_token=workspace.token)
    vantage_sdk.delete_workspace(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_workspace(params)

    # assert that the workspace was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def team_with_description_fixture(vantage_sdk):
    """Fixture to create a team with a description for testing"""
    # setup - create a test team with description
    test_team_name = RESOURCES.team_name
    description = "Test team with description"
    new_team = CreateTeam(
        name=test_team_name,
        description=description,
        workspace_tokens=[settings.workspace_token],
        role=CreateTeamRole.viewer,
        user_tokens=None,
        user_emails=None,
    )

    team: Team = vantage_sdk.create_team(new_team)
    assert team is not None
    assert team.name == test_team_name
    assert team.description == description

    yield team

    # teardown
    params = TeamTokenParams(team_token=team.token)
    vantage_sdk.delete_team(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_team(params)

    # assert that the team was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def access_grant_fixture(vantage_sdk, folder_fixture, team_fixture):
    # setup - create an access grant for a folder
    new_access_grant = CreateAccessGrant(
        resource_token=folder_fixture.token,
        team_token=team_fixture.token,
        access=CreateAccessGrantAccess.allowed,
    )

    access_grant: AccessGrant = vantage_sdk.create_access_grant(new_access_grant)
    assert access_grant is not None
    assert access_grant.resource_token == folder_fixture.token
    assert access_grant.team_token == team_fixture.token
    assert access_grant.access == "allowed"

    yield access_grant

    # teardown
    params = AccessGrantTokenParams(access_grant_token=access_grant.token)
    vantage_sdk.delete_access_grant(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_access_grant(params)

    # assert that the access grant was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def access_grant_denied_fixture(vantage_sdk, folder_fixture, team_fixture):
    """Fixture to create an access grant with denied access"""
    # setup - create an access grant with denied access
    new_access_grant = CreateAccessGrant(
        resource_token=folder_fixture.token,
        team_token=team_fixture.token,
        access=CreateAccessGrantAccess.denied,
    )

    access_grant: AccessGrant = vantage_sdk.create_access_grant(new_access_grant)
    assert access_grant is not None
    assert access_grant.resource_token == folder_fixture.token
    assert access_grant.team_token == team_fixture.token
    assert access_grant.access == "denied"

    yield access_grant

    # teardown
    params = AccessGrantTokenParams(access_grant_token=access_grant.token)
    vantage_sdk.delete_access_grant(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_access_grant(params)

    # assert that the access grant was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def anomaly_notification_fixture(vantage_sdk, cost_report_fixture):
    # setup - create an anomaly notification for a cost report
    new_anomaly_notification = CreateAnomalyNotification(
        cost_report_token=cost_report_fixture.token,
        threshold=1000,
        user_tokens=None,
        recipient_channels=["#test-anomaly-notifications"],
    )

    anomaly_notification: AnomalyNotification = vantage_sdk.create_anomaly_notification(new_anomaly_notification)
    assert anomaly_notification is not None
    assert anomaly_notification.cost_report_token == cost_report_fixture.token
    assert anomaly_notification.threshold == 1000

    yield anomaly_notification

    # teardown
    params = AnomalyNotificationTokenParams(anomaly_notification_token=anomaly_notification.token)
    vantage_sdk.delete_anomaly_notification(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_anomaly_notification(params)

    # assert that the anomaly notification was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def anomaly_notification_threshold_2000_fixture(vantage_sdk, cost_report_fixture):
    """Fixture to create an anomaly notification with threshold 2000"""
    # setup - create an anomaly notification with threshold 2000
    new_anomaly_notification = CreateAnomalyNotification(
        cost_report_token=cost_report_fixture.token,
        threshold=2000,
        user_tokens=None,
        recipient_channels=["#test-anomaly-notifications"],
    )

    anomaly_notification: AnomalyNotification = vantage_sdk.create_anomaly_notification(new_anomaly_notification)
    assert anomaly_notification is not None
    assert anomaly_notification.cost_report_token == cost_report_fixture.token
    assert anomaly_notification.threshold == 2000

    yield anomaly_notification

    # teardown
    params = AnomalyNotificationTokenParams(anomaly_notification_token=anomaly_notification.token)
    vantage_sdk.delete_anomaly_notification(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_anomaly_notification(params)

    # assert that the anomaly notification was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def billing_rule_fixture(vantage_sdk):
    # setup - create a test billing rule
    # Note: This fixture will only work with enterprise accounts that have billing rules enabled
    # This is the structure for when billing rules are available:
    new_billing_rule = CreateBillingRule(
        type="adjustment",
        title="test_billing_rule",
        start_period="2024-01",
        charge_type="Usage",
        service="EC2",
        category="Compute",
        sub_category="Compute Instance",
        amount=100.0,
        percentage=10.0,
        sql_query="SELECT * FROM costs WHERE service = 'EC2'",
    )

    billing_rule: BillingRule = vantage_sdk.create_billing_rule(new_billing_rule)
    assert billing_rule is not None
    assert billing_rule.title == "test_billing_rule"

    yield billing_rule

    # teardown
    params = BillingRuleTokenParams(billing_rule_token=billing_rule.token)
    vantage_sdk.delete_billing_rule(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_billing_rule(params)

    # assert that the billing rule was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture
def create_data_export(vantage_sdk, cost_report_fixture):
    query_params = CostsGetParametersQuery(
        groupings=["service", "provider", "account_id"],
        filter="costs.provider = 'aws'",
        start_date="2024-01-01",
        end_date="2024-01-31",
        date_interval=None,
    )
    request_body = CostsDataExportsPostRequest(
        cost_report_token=cost_report_fixture.token,
        workspace_token=settings.workspace_token,
        schema=CreateCostExportSchema.focus,
    )
    data_export_token: str = vantage_sdk.create_data_export(
        new_data_export=request_body, data_export_query_params=query_params
    )
    print(f"Data export token: {data_export_token}")
    assert data_export_token is not None
    assert data_export_token.startswith("dta_xprt_")
    yield data_export_token


@pytest.fixture()
def saved_filter_fixture(vantage_sdk):
    # setup
    filter_name = RESOURCES.saved_filter_name
    sample_filter = "costs.provider = 'aws'"

    new_saved_filter = CreateSavedFilter(
        title=filter_name, workspace_token=settings.workspace_token, filter=sample_filter
    )

    saved_filter: SavedFilter = vantage_sdk.create_saved_filter(new_saved_filter)
    assert saved_filter is not None
    assert saved_filter.title == filter_name

    yield saved_filter

    # teardown
    params = SavedFilterTokenParams(saved_filter_token=saved_filter.token)
    vantage_sdk.delete_saved_filter(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_saved_filter(params)

    # assert that the saved filter was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def virtual_tag_fixture(vantage_sdk):
    # setup
    tag_key = RESOURCES.virtual_tag_name

    date = datetime.now().strftime("%Y-%m-%d")
    new_virtual_tag = CreateVirtualTagConfig(
        key=tag_key,
        overridable=False,
        backfill_until=date,
        collapsed_tag_keys=[
            CreateVirtualTagConfigCollapsedTagKey(key="team", providers=["aws"]),
        ],
        values=[
            CreateVirtualTagConfigValue(
                filter="costs.provider = 'aws'",
                name="Primary",
            )
        ],
    )

    virtual_tag: VirtualTagConfig = vantage_sdk.create_virtual_tag(new_virtual_tag)
    assert virtual_tag is not None
    assert virtual_tag.key == tag_key

    yield virtual_tag

    # teardown
    params = VirtualTagTokenParams(virtual_tag_token=virtual_tag.token)
    vantage_sdk.delete_virtual_tag(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_virtual_tag(params)

    # assert that the virtual tag was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def business_metric_fixture(vantage_sdk, cost_report_fixture):
    """Fixture to create a business metric for testing"""
    business_metric_name = RESOURCES.business_metric_name
    cost_report_business_metric = CreateBusinessMetricCostReportTokensWithMetadatum(
        cost_report_token=cost_report_fixture.token,
        unit_scale=CreateBusinessMetricCostReportTokensWithMetadatumUnitScale.per_unit,
        label_filter=["env:prod"],
    )
    new_business_metric = CreateBusinessMetric(
        title=business_metric_name,
        cost_report_tokens_with_metadata=[cost_report_business_metric],
        values=[CreateBusinessMetricValue(date=datetime.now().astimezone(), amount=100.0, label="baseline")],
        forecasted_values=[
            CreateBusinessMetricForecastedValue(
                date=datetime.now().astimezone(),
                amount=120.0,
                label="forecast",
            )
        ],
        datadog_metric_fields=None,
        cloudwatch_fields=None,
    )

    business_metric: BusinessMetric = vantage_sdk.create_business_metric(new_business_metric)
    assert business_metric is not None
    assert business_metric.title == business_metric_name

    yield business_metric

    params = BusinessMetricTokenParams(business_metric_token=business_metric.token)
    vantage_sdk.delete_business_metric(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_business_metric(params)

    # Assert that the business metric was deleted
    assert exc_info.value.response.status_code in {404, 502}


@pytest.fixture()
def budget_fixture(vantage_sdk, cost_report_fixture):
    """Fixture to create a budget for testing"""
    # setup - create a test budget
    current_date = datetime.now()

    budget_name = RESOURCES.budget_name
    new_budget = CreateBudget(
        name=budget_name,
        workspace_token=settings.workspace_token,
        cost_report_token=cost_report_fixture.token,
        child_budget_tokens=None,
        periods=[
            CreateBudgetPeriod(
                start_at=current_date.date(),
                end_at=(current_date.date()),
                amount=10000,
            )
        ],
    )

    budget: Budget = vantage_sdk.create_budget(new_budget)
    assert budget is not None
    assert budget.name == budget_name

    yield budget

    # teardown
    params = BudgetTokenParams(budget_token=budget.token)
    vantage_sdk.delete_budget(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_budget(params)

    # assert that the budget was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def budget_alert_fixture(vantage_sdk, budget_fixture):
    """Fixture to create a budget alert for testing"""
    # Note: Budget alerts require workspace configuration that may not be available in all test environments
    # setup - create a test budget alert
    users = vantage_sdk.get_all_users()
    user_token = users.users[0].token

    new_budget_alert = BudgetAlertsPostRequest(
        budget_tokens=[budget_fixture.token],
        threshold=50,
        duration_in_days="30",
        workspace_token=settings.workspace_token,
        user_tokens=[user_token],
    )

    budget_alert: BudgetAlert = vantage_sdk.create_budget_alert(new_budget_alert)
    assert budget_alert is not None
    assert budget_fixture.token in budget_alert.budget_tokens
    assert budget_alert.threshold == 50

    yield budget_alert

    # teardown
    params = BudgetAlertTokenParams(budget_alert_token=budget_alert.token)
    vantage_sdk.delete_budget_alert(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_budget_alert(params)

    # assert that the budget alert was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def dashboard_fixture(vantage_sdk, cost_report_fixture):
    """Fixture to create a dashboard for testing"""

    # setup - create a test dashboard
    dashboard_title = RESOURCES.dashboard_name

    new_dashboard = CreateDashboard(
        title=dashboard_title,
        widgets=[
            CreateDashboardWidget(
                widgetable_token=cost_report_fixture.token,
                title=f"{dashboard_title}_widget",
                settings=CreateDashboardWidgetSettings(display_type="table"),
            )
        ],
        saved_filter_tokens=None,
        date_bin=CreateDashboardDateBin.month,
        date_interval=CreateDashboardDateInterval.last_30_days,
        start_date=None,
        end_date=None,
        workspace_token=settings.workspace_token,
    )

    dashboard: Dashboard = vantage_sdk.create_dashboard(new_dashboard)
    assert dashboard is not None
    assert dashboard.title == dashboard_title

    yield dashboard

    # teardown
    params = DashboardTokenParams(dashboard_token=dashboard.token)
    vantage_sdk.delete_dashboard(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_dashboard(params)

    # assert that the dashboard was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def cost_alert_fixture(vantage_sdk, cost_report_fixture):
    """Fixture to create a cost alert for testing"""
    # setup - create a test cost alert
    cost_alert_name = RESOURCES.cost_alert_name
    new_cost_alert = CreateCostAlert(
        workspace_token=settings.workspace_token,
        title=cost_alert_name,
        interval="month",
        threshold=1000,
        unit_type="currency",
        report_tokens=[cost_report_fixture.token],
        email_recipients=None,
        slack_channels=None,
        teams_channels=None,
        minimum_threshold=None,
    )

    cost_alert: CostAlert = vantage_sdk.create_cost_alert(new_cost_alert)
    assert cost_alert is not None
    assert cost_alert.title == cost_alert_name
    assert cost_alert.threshold == 1000
    assert cost_alert.interval == "month"
    assert cost_alert.unit_type == "currency"

    yield cost_alert

    # teardown
    params = CostAlertTokenParams(cost_alert_token=cost_alert.token)
    vantage_sdk.delete_cost_alert(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_cost_alert(params)

    # assert that the cost alert was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def financial_commitment_report_fixture(vantage_sdk):
    """Fixture to create a financial commitment report for testing"""
    # setup - create a test financial commitment report
    report_name = RESOURCES.financial_commitment_report_name
    new_financial_commitment_report = CreateFinancialCommitmentReport(
        title=report_name,
        workspace_token=settings.workspace_token,
        filter=None,
        date_interval=CreateFinancialCommitmentReportDateInterval.last_3_months,
        date_bucket=None,
        on_demand_costs_scope=None,
        groupings=None,
    )

    financial_commitment_report: FinancialCommitmentReport = vantage_sdk.create_financial_commitment_report(
        new_financial_commitment_report
    )
    assert financial_commitment_report is not None
    assert financial_commitment_report.title == report_name

    yield financial_commitment_report

    # teardown
    params = FinancialCommitmentReportTokenParams(financial_commitment_report_token=financial_commitment_report.token)
    vantage_sdk.delete_financial_commitment_report(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_financial_commitment_report(params)

    # assert that the financial commitment report was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def kubernetes_efficiency_report_fixture(vantage_sdk):
    """Fixture to create a kubernetes efficiency report for testing"""
    # setup - create a test kubernetes efficiency report
    report_name = RESOURCES.kubernetes_efficiency_report_name
    new_kubernetes_efficiency_report = CreateKubernetesEfficiencyReport(
        title=report_name,
        workspace_token=settings.workspace_token,
        date_interval=CreateKubernetesEfficiencyReportDateInterval.this_month,
        aggregated_by=None,
        date_bucket=None,
        groupings=None,
    )

    kubernetes_efficiency_report: KubernetesEfficiencyReport = vantage_sdk.create_kubernetes_efficiency_report(
        new_kubernetes_efficiency_report
    )
    assert kubernetes_efficiency_report is not None
    assert kubernetes_efficiency_report.title == report_name

    yield kubernetes_efficiency_report

    # teardown
    params = KubernetesEfficiencyReportTokenParams(
        kubernetes_efficiency_report_token=kubernetes_efficiency_report.token
    )
    vantage_sdk.delete_kubernetes_efficiency_report(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_kubernetes_efficiency_report(params)

    # assert that the kubernetes efficiency report was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def managed_account_fixture(vantage_sdk):
    """Fixture to create a managed account for testing"""
    # setup - create a test managed account
    account_name = RESOURCES.managed_account_name
    contact_email = "test@example.com"

    new_managed_account = CreateManagedAccount(
        name=account_name,
        contact_email=contact_email,
        access_credential_tokens=None,
        billing_rule_tokens=None,
        email_domain="example.com",
    )

    managed_account: ManagedAccount = vantage_sdk.create_managed_account(new_managed_account)
    assert managed_account is not None
    assert managed_account.name == account_name
    assert managed_account.contact_email == contact_email

    yield managed_account

    # teardown
    params = ManagedAccountTokenParams(managed_account_token=managed_account.token)
    vantage_sdk.delete_managed_account(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_managed_account(params)

    # assert that the managed account was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def network_flow_report_fixture(vantage_sdk):
    """Fixture to create a network flow report for testing"""
    # setup - create a test network flow report
    report_name = RESOURCES.network_flow_report_name
    new_network_flow_report = CreateNetworkFlowReport(
        title=report_name,
        workspace_token=settings.workspace_token,
        filter=None,
        date_interval=CreateNetworkFlowReportDateInterval.last_7_days,
        groupings=[CreateNetworkFlowReportGrouping.region],
        flow_direction=CreateNetworkFlowReportFlowDirection.ingress,
        flow_weight=CreateNetworkFlowReportFlowWeight.costs,
    )

    network_flow_report: NetworkFlowReport = vantage_sdk.create_network_flow_report(new_network_flow_report)
    assert network_flow_report is not None
    assert network_flow_report.title == report_name

    yield network_flow_report

    # teardown
    params = NetworkFlowReportTokenParams(network_flow_report_token=network_flow_report.token)
    vantage_sdk.delete_network_flow_report(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_network_flow_report(params)

    # assert that the network flow report was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture()
def resource_report_fixture(vantage_sdk):
    """Fixture to create a resource report for testing"""
    # setup - create a test resource report
    report_name = RESOURCES.resource_report_name
    new_resource_report = CreateResourceReport(
        title=report_name,
        workspace_token=settings.workspace_token,
        filter=None,
        columns=None,
    )

    resource_report: ResourceReport = vantage_sdk.create_resource_report(new_resource_report)
    assert resource_report is not None
    assert resource_report.title == report_name

    yield resource_report

    # teardown
    params = ResourceReportTokenParams(resource_report_token=resource_report.token)
    vantage_sdk.delete_resource_report(params)

    with pytest.raises(HTTPError) as exc_info:
        vantage_sdk.get_resource_report(params)

    # assert that the resource report was deleted
    assert exc_info.value.response.status_code == 404


@pytest.fixture
def cost_report_audit_log_fixture(vantage_sdk, cost_report_fixture):
    """
    Fixture that ensures a cost report has at least one audit log, uses
    the cost_report_fixture which handles creation/deletion of the report
    to force an audit log entry by updating the report.

    NOTE: API-initiated actions seemingly default to the organization's primary workspace
    for audit logging, even if the resource was created in a specific workspace
    Therefore, we filter ONLY by object_token and NOT by workspace_token to ensure we find the logs
    """
    # Trigger an audit log by updating the cost report
    updated_title = f"{RESOURCES.updated_prefix}_{cost_report_fixture.title}"
    cost_report_update = UpdateCostReport(title=updated_title)
    params = CostReportTokenParams(cost_report_token=cost_report_fixture.token)
    _ = vantage_sdk.update_cost_report(params, cost_report_update)

    audit_log_params = AuditLogsGetParametersQuery(object_token=cost_report_fixture.token)
    audit_logs: AuditLogs = vantage_sdk.get_all_audit_logs(audit_log_params)

    assert audit_logs.audit_logs is not None

    yield audit_logs, cost_report_fixture.token
