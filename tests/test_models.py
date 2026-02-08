from collections.abc import Callable
from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkspaceConfig(BaseModel):
    """Workspace configuration with token information"""

    env_path: Path = Field(Path(__file__).parent.parent / ".env", description="Path to environment file")


WORKSPACE = WorkspaceConfig()


class Settings(BaseSettings):
    """Settings for Vantage API client"""

    model_config = SettingsConfigDict(env_file=WORKSPACE.env_path, env_file_encoding="utf-8")
    vantage_api_key: str
    workspace_token: str
    vcr_enabled: bool = False


class ResourcePrefix(str, Enum):
    """Enum for resource name prefixes"""

    FOLDER = "test_folder"
    COST_REPORT = "test_cost_report"
    SAVED_FILTER = "test_filter"
    VIRTUAL_TAG = "test_vtag"
    BUSINESS_METRIC = "test_business_metric"
    INTEGRATION = "test_integration"
    BUDGET = "test_budget"
    COST_ALERT = "test_cost_alert"
    DASHBOARD = "test_dashboard"
    FINANCIAL_COMMITMENT_REPORT = "test_fin_commitment_report"
    KUBERNETES_EFFICIENCY_REPORT = "test_k8s_efficiency_report"
    MANAGED_ACCOUNT = "test_managed_account"
    NETWORK_FLOW_REPORT = "test_network_flow_report"
    RESOURCE_REPORT = "test_resource_report"
    TAG = "test_tag"
    TEAM = "test_team"
    WORKSPACE = "test_workspace"
    UPDATED = "updated"


class ResourceNameFactory(BaseModel):
    """Test resource name generator and container"""

    name_generator: Callable[[str], str] = Field(default_factory=lambda: ResourceNameFactory._build_name)

    @staticmethod
    def _build_name(prefix: str) -> str:
        if Settings().vcr_enabled:
            return f"{prefix.value}_vcr"
        return f"{prefix.value}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

    @property
    def team_name(self) -> str:
        return self.name_generator(ResourcePrefix.TEAM)

    @property
    def workspace_name(self) -> str:
        return self.name_generator(ResourcePrefix.WORKSPACE)

    @property
    def folder_name(self) -> str:
        return self.name_generator(ResourcePrefix.FOLDER)

    @property
    def cost_report_name(self) -> str:
        return self.name_generator(ResourcePrefix.COST_REPORT)

    @property
    def saved_filter_name(self) -> str:
        return self.name_generator(ResourcePrefix.SAVED_FILTER)

    @property
    def virtual_tag_name(self) -> str:
        return self.name_generator(ResourcePrefix.VIRTUAL_TAG)

    @property
    def business_metric_name(self) -> str:
        return self.name_generator(ResourcePrefix.BUSINESS_METRIC)

    @property
    def integration_name(self) -> str:
        return self.name_generator(ResourcePrefix.INTEGRATION)

    @property
    def budget_name(self) -> str:
        return self.name_generator(ResourcePrefix.BUDGET)

    @property
    def cost_alert_name(self) -> str:
        return self.name_generator(ResourcePrefix.COST_ALERT)

    @property
    def dashboard_name(self) -> str:
        return self.name_generator(ResourcePrefix.DASHBOARD)

    @property
    def financial_commitment_report_name(self) -> str:
        return self.name_generator(ResourcePrefix.FINANCIAL_COMMITMENT_REPORT)

    @property
    def kubernetes_efficiency_report_name(self) -> str:
        return self.name_generator(ResourcePrefix.KUBERNETES_EFFICIENCY_REPORT)

    @property
    def managed_account_name(self) -> str:
        return self.name_generator(ResourcePrefix.MANAGED_ACCOUNT)

    @property
    def network_flow_report_name(self) -> str:
        return self.name_generator(ResourcePrefix.NETWORK_FLOW_REPORT)

    @property
    def resource_report_name(self) -> str:
        return self.name_generator(ResourcePrefix.RESOURCE_REPORT)

    @property
    def tag_name(self) -> str:
        return self.name_generator(ResourcePrefix.TAG)

    @property
    def updated_prefix(self) -> str:
        return self.name_generator(ResourcePrefix.UPDATED)
