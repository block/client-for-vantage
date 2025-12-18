import asyncio
import logging
import warnings
from collections.abc import Sequence
from typing import NewType, TypeVar
from urllib.parse import urljoin

from httpx import AsyncClient, Client, HTTPError, HTTPStatusError, Timeout
from pydantic import BaseModel

from vantage_sdk.models import (
    AccessGrant,
    AccessGrants,
    AccessGrantTokenParams,
    AnomalyAlert,
    AnomalyAlerts,
    AnomalyAlertsGetParametersQuery,
    AnomalyAlertTokenParams,
    AnomalyNotification,
    AnomalyNotifications,
    AnomalyNotificationTokenParams,
    AuditLog,
    AuditLogs,
    AuditLogsGetParametersQuery,
    AuditLogTokenParams,
    BillingRule,
    BillingRules,
    BillingRuleTokenParams,
    Budget,
    BudgetAlert,
    BudgetAlerts,
    BudgetAlertsBudgetAlertTokenPutRequest,
    BudgetAlertsPostRequest,
    BudgetAlertTokenParams,
    Budgets,
    BudgetsBudgetTokenGetParametersQuery,
    BudgetTokenParams,
    BusinessMetric,
    BusinessMetrics,
    BusinessMetricsBusinessMetricTokenValuesGetParametersQuery,
    BusinessMetricTokenParams,
    BusinessMetricValues,
    CostAlert,
    CostAlertEvent,
    CostAlertEvents,
    CostAlertEventTokenParams,
    CostAlerts,
    CostAlertsCostAlertTokenEventsGetParametersQuery,
    CostAlertTokenParams,
    CostProviders,
    CostReport,
    CostReports,
    CostReportsCostReportTokenForecastedCostsGetParametersQuery,
    CostReportTokenParams,
    Costs,
    CostsDataExportsPostParametersQuery,
    CostsDataExportsPostRequest,
    CostServices,
    CostsGetParametersQuery,
    CreateAccessGrant,
    CreateAnomalyNotification,
    CreateAzureIntegration,
    CreateBillingRule,
    CreateBudget,
    CreateBusinessMetric,
    CreateCostAlert,
    CreateCostReport,
    CreateCustomProviderIntegration,
    CreateDashboard,
    CreateFinancialCommitmentReport,
    CreateFolder,
    CreateGCPIntegration,
    CreateKubernetesEfficiencyReport,
    CreateManagedAccount,
    CreateNetworkFlowReport,
    CreateReportNotification,
    CreateResourceReport,
    CreateSavedFilter,
    CreateSegment,
    CreateTeam,
    CreateUserFeedback,
    CreateVirtualTagConfig,
    CreateWorkspace,
    Dashboard,
    Dashboards,
    DashboardsGetParametersQuery,
    DashboardTokenParams,
    DataExport,
    DataExportTokenParams,
    FinancialCommitmentReport,
    FinancialCommitmentReports,
    FinancialCommitmentReportTokenParams,
    FinancialCommitments,
    Folder,
    Folders,
    FolderTokenParams,
    ForecastedCosts,
    Integration,
    Integrations,
    IntegrationsGetParametersQuery,
    IntegrationsIntegrationTokenPutRequest,
    IntegrationTokenParams,
    KubernetesEfficiencyReport,
    KubernetesEfficiencyReports,
    KubernetesEfficiencyReportTokenParams,
    ManagedAccount,
    ManagedAccounts,
    ManagedAccountTokenParams,
    Me,
    NetworkFlowReport,
    NetworkFlowReports,
    NetworkFlowReportTokenParams,
    Price,
    Prices,
    Product,
    ProductIdParams,
    ProductPriceIdParams,
    Products,
    Recommendation,
    RecommendationResource,
    RecommendationResources,
    RecommendationResourceTokenParams,
    Recommendations,
    RecommendationTokenParams,
    ReportNotification,
    ReportNotifications,
    ReportNotificationTokenParams,
    Resource,
    ResourceReport,
    ResourceReports,
    ResourceReportTokenParams,
    Resources,
    ResourcesGetParametersQuery,
    ResourceTokenParams,
    SavedFilter,
    SavedFilters,
    SavedFilterTokenParams,
    Segment,
    Segments,
    SegmentTokenParams,
    Tag,
    TagKeyParams,
    Tags,
    TagsGetParametersQuery,
    TagsKeyValuesGetParametersQuery,
    TagValues,
    Team,
    Teams,
    TeamTokenParams,
    UnitCosts,
    UnitCostsDataExportsPostRequest,
    UnitCostsGetParametersQuery,
    UpdateAccessGrant,
    UpdateAnomalyAlert,
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
    UpdateReportNotification,
    UpdateResourceReport,
    UpdateSegment,
    UpdateTag,
    UpdateTeam,
    UpdateVirtualTagConfig,
    User,
    UserCostsUploads,
    UserFeedback,
    Users,
    UserTokenParams,
    VirtualTagConfig,
    VirtualTagConfigs,
    VirtualTagTokenParams,
    Workspace,
    Workspaces,
    WorkspacesGetParametersQuery,
    WorkspacesWorkspaceTokenPutRequest,
    WorkspaceTokenParams,
)

logger = logging.getLogger(__name__)

# ---- Types ----

# Http status code
HttpStatusCode = NewType("HttpStatusCode", int)
PollInterval = NewType("PollInterval", int)
# Generic type
T = TypeVar("T")
# This type accepts only BaseModel subclasses
BaseModelType = TypeVar("BaseModelType", bound=BaseModel)

# ---- Consts ----

# Base URL for the Vantage API
BASE_URL = "https://api.vantage.sh/v2/"


class VantageSDK:
    """VantageSDK is a Python client for the Vantage API"""

    _timeout = Timeout(60.0, read=None)

    def __init__(self, api_key: str, session: Client | None = None):
        self.base_url = BASE_URL
        # Preventing mutable default arguments
        if session is None:
            session = Client()
        self.session = session
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )

    # ---- Private Methods ----

    def _get(self, endpoint: str, params: dict | BaseModel | None = None) -> dict:
        """
        Perform a GET request to the specified endpoint

        Args:
            endpoint: The API endpoint to fetch data from
            params: Optional query parameters for the request, must be a Pydantic model

        Returns:
            The JSON response from the API
        """
        url = urljoin(self.base_url, endpoint)

        if isinstance(params, BaseModel):
            params = params.model_dump(
                mode="json",
                by_alias=True,
                exclude_none=True,
                exclude_defaults=True,
            )

        response = self.session.get(url, params=params, timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def _get_paginated(self, endpoint: str, params: dict | BaseModel | None = None) -> dict:
        """Fetch paginated results automatically, combining all pages into a single response dictionary

        Logic:
            If the response is not paginated, the result fails fast and raises an exception
            If any of the requests fail, the entire operation fails and raises an exception,
            so that partial data is not returned

        Args:
            endpoint: The API endpoint to fetch data from
            params: Optional query parameters for the request, can be a Pydantic model or dict

        Returns:
            The combined response from all pages
        """
        # Initialize params if needed
        if params is None:
            params = {}
        elif isinstance(params, BaseModel):
            params = params.model_dump(mode="json", exclude_none=True, exclude_defaults=True)

        first_response = self._get(endpoint, {**params, "page": 1})

        def parse_page(page_response: dict, page_key: str) -> int | None:
            links = page_response.get("links", {}).get(page_key, None)
            if links:
                return int(links.split("page=")[1])
            return None

        total_pages = parse_page(first_response, "last")
        next_page = parse_page(first_response, "next")

        # If a normal paginated response returns 1 for total_pages, there is only one page
        # or if the GET /costs endpoint returns None for total_pages and next_page
        if total_pages == 1 or (total_pages is None and next_page is None):
            first_response.pop("links", None)
            return first_response

        # Identify keys to merge (excluding links)
        response_keys = [k for k in first_response if k != "links"]

        # GET /costs is the only paginated endpoint that returns None for total_pages
        # since Vantage doesn't provide the total number of pages
        # We don't know total pages, so fetch next pages in sequence
        if not total_pages:
            while next_page:
                page_data = self._get(endpoint, {**params, "page": next_page})
                for key in response_keys:
                    if key in page_data:
                        if isinstance(first_response[key], list) and isinstance(page_data[key], list):
                            first_response[key].extend(page_data[key])
                            logger.debug(
                                "Page %d: Added %d items to list key '%s'", next_page, len(page_data[key]), key
                            )
                        elif isinstance(first_response[key], dict) and isinstance(page_data[key], dict):
                            first_response[key].update(page_data[key])
                            logger.debug("Page %d: Updated dictionary key '%s'", next_page, key)
                    else:
                        # For other types, assume addition is appropriate
                        first_response[key] += page_data[key]
                        logger.debug("Page %d: Updated scalar key '%s'", next_page, key)

                next_page = parse_page(page_data, "next")

            first_response.pop("links", None)
            return first_response

        async def fetch_remaining_pages() -> None:
            """Fetch all remaining pages concurrently"""
            # Create a temporary async client with the same headers
            headers = dict(self.session.headers)

            # Initialize a new async client
            async with AsyncClient(base_url=self.base_url, headers=headers, timeout=self._timeout) as async_client:
                # Create tasks for pages 2 to n
                tasks = []

                for page_num in range(2, total_pages + 1):
                    page_params = {**params, "page": page_num}
                    tasks.append(async_client.get(f"/{endpoint}", params=page_params))

                    # Log URLs for debugging
                    query_string = "&".join([f"{k}={v}" for k, v in page_params.items()])
                    full_url = f"{self.base_url}/{endpoint}?{query_string}"
                    logger.debug("Fetching page %d: %s", page_num, full_url)

                # Execute all requests concurrently
                responses = await asyncio.gather(*tasks, return_exceptions=True)

                # Process results
                for i, response in enumerate(responses, start=2):
                    # Check if response is an exception
                    if isinstance(response, Exception):
                        error_msg = f"Request failed for page {i}: {response!s}"
                        logger.error(error_msg)
                        raise RuntimeError(error_msg)

                    # Check for HTTP errors
                    if response.is_error:  # type: ignore
                        error_msg = f"HTTP error on page {i}: {response.status_code} - {response.text}"  # type: ignore
                        logger.error(error_msg)
                        raise RuntimeError(error_msg)

                    page_data = response.json()  # type: ignore

                    # Process each key from the response
                    for key in response_keys:
                        if key in page_data:
                            if isinstance(first_response[key], list) and isinstance(page_data[key], list):
                                first_response[key].extend(page_data[key])
                                logger.debug("Page %d: Added %d items to list key '%s'", i, len(page_data[key]), key)
                            elif isinstance(first_response[key], dict) and isinstance(page_data[key], dict):
                                first_response[key].update(page_data[key])
                                logger.debug("Page %d: Updated dictionary key '%s'", i, key)
                            else:
                                # For other types, assume addition is appropriate
                                first_response[key] += page_data[key]
                                logger.debug("Page %d: Updated scalar key '%s'", i, key)

        # Run the async function
        asyncio.run(fetch_remaining_pages())

        # Remove the links from the result
        first_response.pop("links", None)

        return first_response

    def _post(self, endpoint: str, params: BaseModelType) -> dict:
        """
        Perform a POST request to the specified endpoint

        Args:
            endpoint: The API endpoint to post data to
            params: The Pydantic model to serialize and send

        Returns:
            The JSON response from the API
        """
        url = urljoin(self.base_url, endpoint)

        if isinstance(params, BaseModel):
            json_data = params.model_dump(
                mode="json",
                by_alias=True,
                exclude_none=True,
                exclude_defaults=True,
            )
        else:
            json_data = params

        response = self.session.post(url, json=json_data)
        response.raise_for_status()
        return response.json()

    def _put(self, endpoint: str, params: BaseModelType) -> dict:
        """
        Perform a PUT request to the specified endpoint

        Args:
            endpoint: The API endpoint to update data
            params: The Pydantic model to serialize and send

        Returns:
            The JSON response from the API
        """
        url = urljoin(self.base_url, endpoint)

        if isinstance(params, BaseModel):
            json_data = params.model_dump(
                mode="json",
                by_alias=True,
                exclude_none=True,
                exclude_defaults=True,
            )
        else:
            json_data = params

        response = self.session.put(url, json=json_data)
        response.raise_for_status()
        return response.json()

    def _delete(self, endpoint: str) -> HttpStatusCode:
        """
        Perform a DELETE request to the specified endpoint

        Args:
            endpoint: The API endpoint to delete data

        Returns:
            The HTTP status code of the response
        """
        url = urljoin(self.base_url, endpoint)
        response = self.session.delete(url)
        response.raise_for_status()
        return HttpStatusCode(response.status_code)

    # ---- Folder APIs ----

    def get_all_folders(self) -> Folders:
        """
        Get all folders - GET /folders

        Returns:
            A Folders object which is a list of Folder objects

        """
        # getting all folders
        paginated_data = self._get_paginated("folders")
        return Folders.model_validate(paginated_data)

    def create_folder(self, new_folder: CreateFolder) -> Folder:
        """
        Create a new folder - POST /folders

        Args:
            new_folder: The new folder object to create

        Returns:
            The created folder object
        """
        data = self._post("folders", new_folder)
        return Folder.model_validate(data)

    def get_folder(self, folder_token_params: FolderTokenParams) -> Folder:
        """
        Retrieve a specific folder - GET /folders/{folder_token}

        Args:
            folder_token_params: The token of the folder to retrieve, begins with 'fldr_'

        Returns:
            The folder object
        """
        folder_value = folder_token_params.folder_token
        data = self._get(f"folders/{folder_value}")
        return Folder.model_validate(data)

    def update_folder(self, folder_token_params: FolderTokenParams, folder_update: UpdateFolder) -> Folder:
        """
        Update a specific folder - PUT /folders/{folder_token}

        Args:
            folder_token_params: The token of the folder to update, begins with 'fldr_'
            folder_update: The updated folder object

        Returns:
            The updated folder object
        """
        folder_value = folder_token_params.folder_token
        data = self._put(f"folders/{folder_value}", folder_update)
        return Folder.model_validate(data)

    def delete_folder(self, folder_token_params: FolderTokenParams) -> HttpStatusCode:
        """
        Delete a specific folder - DELETE /folders/{folder_token}

        Args:
            folder_token_params: The token of the folder to delete, begins with 'fldr_'

        Returns:
            The HTTP status code of the response
        """
        folder_value = folder_token_params.folder_token
        return self._delete(f"folders/{folder_value}")

    # ---- Cost APIs ----

    def get_all_cost_reports(self, folder_token_params: FolderTokenParams | None = None) -> CostReports:
        """
        Fetch cost reports - GET /cost_reports

        Args:
            folder_token_params: The token of the folder to fetch cost reports from, begins with 'fldr_'

        Returns:
            A list of CostReport objects
        """
        paginated_data = self._get_paginated("cost_reports", folder_token_params)
        return CostReports.model_validate(paginated_data)

    def create_cost_report(self, new_cost_report: CreateCostReport) -> CostReport:
        """
        Create a new cost report - POST /cost_reports

        Args:
            new_cost_report: The new cost report object to create

        Returns:
            The created cost report
        """
        data = self._post("cost_reports", new_cost_report)
        return CostReport.model_validate(data)

    def get_cost_report(self, cost_report_token_params: CostReportTokenParams) -> CostReport:
        """
        Retrieve a specific cost report - GET /cost_reports/{cost_report_token}

        Args:
            cost_report_token_params: The token of the cost report to retrieve, begins with 'rprt_'

        Returns:
            The cost report object
        """
        token_value = cost_report_token_params.cost_report_token
        data = self._get(f"cost_reports/{token_value}")
        return CostReport.model_validate(data)

    def update_cost_report(
        self, cost_report_token_params: CostReportTokenParams, cost_report_update: UpdateCostReport
    ) -> CostReport:
        """
        Update a specific cost report - PUT /cost_reports/{cost_report_token}

        Args:
            cost_report_token_params: The token of the cost report to update, begins with 'rprt_'
            cost_report_update: The updated cost report object

        Returns:
            The updated cost report object
        """
        token_value = cost_report_token_params.cost_report_token
        data = self._put(f"cost_reports/{token_value}", cost_report_update)
        return CostReport.model_validate(data)

    def delete_cost_report(self, cost_report_token_params: CostReportTokenParams) -> HttpStatusCode:
        """
        Delete a specific cost report - DELETE /cost_reports/{cost_report_token}

        Args:
            cost_report_token_params: The token of the cost report to delete, begins with 'rprt_'

        Returns:
            The HTTP status code of the response
        """
        token_value = cost_report_token_params.cost_report_token
        return self._delete(f"cost_reports/{token_value}")

    def get_cost_report_costs(self, cost_report_params: CostsGetParametersQuery) -> Costs:
        """
        Get all costs - GET /costs

        Args:
            cost_report_params: The parameters to filter costs

        Returns:
            A Costs object
        """
        warnings.warn(
            "This endpoint has a very low rate limit \n"
            "Consider implementing a delay or backoff \n"
            "The rate limit is 5 requests every 5 seconds",
            UserWarning,
            2,
        )
        paginated_data = self._get_paginated("costs", cost_report_params)
        return Costs.model_validate(paginated_data)

    # ---- Data Export APIs ----

    def create_data_export(
        self,
        new_data_export: CostsDataExportsPostRequest,
        data_export_query_params: CostsDataExportsPostParametersQuery | None = None,
    ) -> str:
        """
        Create a new data export - POST /costs/data_exports

        Args:
            new_data_export: The new data export object to create
            data_export_query_params: Optional query parameters for the data export

        Returns:
            str: The token of the created data export

        Note:
            This function doesn't use the _post protected method because we
            need to extract the token from the response header
            and not the response body.
            1. The response body is empty
            2. The token is in the 'location' header
        """
        response = self.session.post(
            urljoin(self.base_url, "costs/data_exports"),
            json=new_data_export.model_dump(exclude_none=True, by_alias=True),
            params=data_export_query_params.model_dump(exclude_none=True, by_alias=True)
            if data_export_query_params
            else None,
            headers=self.session.headers,
            timeout=self._timeout,
        )
        if response.is_success:
            location = response.headers["location"]
            # Split the entire location URL and get the last part
            token = location.split("/")[-1]
            data_export_token_params = DataExportTokenParams(data_export_token=token)
            return data_export_token_params.data_export_token
        else:
            error_details = response.json()
            error_message = f"Failed to create data export: {response.status_code}. Details: {error_details}"
            raise HTTPStatusError(error_message, request=response.request, response=response)

    def get_data_export(self, data_export_token_params: DataExportTokenParams) -> DataExport | PollInterval:
        """
        Retrieve a specific data export - GET /data_exports/{data_export_token}

        Args:
            data_export_token_params: The token of the data export to retrieve, begins with 'rprt_'

        Returns:
            DataExport: The data export object
            PollInterval: The number of seconds to wait before polling again if the export is still in progress

        Note:
            This function returns the data export object if it's ready
            If the data export is still in progress, it returns the retry-after value from the response headers
            This is useful for polling the status of the data export
        """
        token_value = data_export_token_params.data_export_token
        response = self.session.get(
            urljoin(self.base_url, f"data_exports/{token_value}"), headers=self.session.headers, timeout=self._timeout
        )

        if response.is_success:
            body = response.json()
            if body == 202:
                # The export is still in progress
                return PollInterval(int(response.headers["retry-after"]))
            else:
                # The export is ready
                return DataExport.model_validate(body)
        else:
            error_details = response.json()
            error_message = f"Failed to create data export: {response.status_code}. Details: {error_details}"
            raise HTTPStatusError(error_message, request=response.request, response=response)

    # ---- Virtual Tag APIs ----

    def create_virtual_tag(self, new_virtual_tag: CreateVirtualTagConfig) -> VirtualTagConfig:
        """
        Create a new custom tag - POST /virtual_tag_configs

        Args:
            new_virtual_tag: The new custom tag object to create

        Returns:
            The created custom tag
        """
        data = self._post("virtual_tag_configs", new_virtual_tag)
        return VirtualTagConfig.model_validate(data)

    def delete_virtual_tag(self, virtual_tag_token_params: VirtualTagTokenParams) -> HttpStatusCode:
        """
        Delete a specific custom tag - DELETE /virtual_tag_configs/{token}

        Args:
            virtual_tag_token_params: The token of the custom tag to delete, begins with 'vtag_'

        Returns:
            The HTTP status code of the response
        """
        virtual_tag_value = virtual_tag_token_params.virtual_tag_token
        return self._delete(f"virtual_tag_configs/{virtual_tag_value}")

    def get_virtual_tag(self, virtual_tag_token_params: VirtualTagTokenParams) -> VirtualTagConfig:
        """
        Retrieve a specific custom tag - GET /virtual_tag_configs/{token}

        Args:
            virtual_tag_token_params: The token of the custom tag to retrieve, begins with 'vtag_'

        Returns:
            The custom tag object
        """
        virtual_tag_value = virtual_tag_token_params.virtual_tag_token
        data = self._get(f"virtual_tag_configs/{virtual_tag_value}")
        return VirtualTagConfig.model_validate(data)

    def get_all_virtual_tags(self) -> VirtualTagConfigs:
        """
        Get all custom tags - GET /virtual_tag_configs

        Returns:
            A list of VirtualTagConfig objects

        Note:
            This method is not paginated
        """
        data = self._get("virtual_tag_configs")
        return VirtualTagConfigs.model_validate(data)

    def update_virtual_tag(
        self, virtual_tag_token_params: VirtualTagTokenParams, virtual_tag_update: UpdateVirtualTagConfig
    ) -> VirtualTagConfig:
        """
        Update a specific custom tag - PUT /virtual_tag_configs/{token}

        Args:
            virtual_tag_token_params: The token of the custom tag to update, begins with 'vtag_'
            virtual_tag_update: The updated custom tag object

        Returns:
            The updated custom tag object
        """
        virtual_tag_value = virtual_tag_token_params.virtual_tag_token
        data = self._put(f"virtual_tag_configs/{virtual_tag_value}", virtual_tag_update)
        return VirtualTagConfig.model_validate(data)

    # ---- Saved Filters APIs ----

    def create_saved_filter(self, new_saved_filter: CreateSavedFilter) -> SavedFilter:
        """
        Create a new saved filter - POST /saved_filters

        Args:
            new_saved_filter: The new saved filter object to create

        Returns:
            The created saved filter
        """
        data = self._post("saved_filters", new_saved_filter)
        return SavedFilter.model_validate(data)

    def delete_saved_filter(self, saved_filter_token_params: SavedFilterTokenParams) -> HttpStatusCode:
        """
        Delete a specific saved filter - DELETE /saved_filters/{saved_filter_token}

        Args:
            saved_filter_token_params: The token of the saved filter to delete, begins with 'svd_fltr'

        Returns:
            The HTTP status code of the response
        """
        saved_filter_value = saved_filter_token_params.saved_filter_token
        return self._delete(f"saved_filters/{saved_filter_value}")

    def get_saved_filter(self, saved_filter_token_params: SavedFilterTokenParams) -> SavedFilter:
        """
        Retrieve a specific saved filter - GET /saved_filters/{saved_filter_token}

        Args:
            saved_filter_token_params: The token of the saved filter to retrieve, begins with 'svd_fltr'

        Returns:
            The saved filter object
        """
        saved_filter_value = saved_filter_token_params.saved_filter_token
        data = self._get(f"saved_filters/{saved_filter_value}")
        return SavedFilter.model_validate(data)

    def get_all_saved_filters(self) -> SavedFilters:
        """
        Get all saved filters - GET /saved_filters

        Returns:
            A list of SavedFilter objects
        """
        paginated_data = self._get_paginated("saved_filters")
        return SavedFilters.model_validate(paginated_data)

    # ---- Health Check ----

    def ping(self) -> bool:
        """
        Ping the 'ping' URL to verify connectivity

        Returns:
            True if the response is "pong", False otherwise
        """
        try:
            response = self._get("ping")
            return response["ping"] == "pong"
        except HTTPError:
            return False

    # ---- Business Metrics ----

    def create_business_metric(self, new_business_metric: CreateBusinessMetric) -> BusinessMetric:
        """
        Create a new business metric - POST /business_metrics

        Args:
            new_business_metric: The new business metric object to create

        Returns:
            A BusinessMetric object
        """
        data = self._post("business_metrics", new_business_metric)
        return BusinessMetric.model_validate(data)

    def get_all_business_metrics(self) -> BusinessMetrics:
        """
        Get all business metrics - GET /business_metrics

        Returns:
            A BusinessMetrics object which is a list of BusinessMetric objects
        """
        paginated_data = self._get_paginated("business_metrics")
        return BusinessMetrics.model_validate(paginated_data)

    def get_business_metric(self, business_metric_token: BusinessMetricTokenParams) -> BusinessMetric:
        """
        Get a specific business metric - GET /business_metrics/{business_metric_token}

        Args:
            business_metric_token: The token of the business metric to retrieve

        Returns:
            The business metric object
        """
        business_metric_token_value = business_metric_token.business_metric_token
        data = self._get(f"business_metrics/{business_metric_token_value}")
        return BusinessMetric.model_validate(data)

    def delete_business_metric(self, business_metric_token: BusinessMetricTokenParams) -> HttpStatusCode:
        """
        Delete a specific business metric - DELETE /business_metrics/{business_metric_token}

        Args:
            business_metric_token: The token of the business metric to delete

        Returns:
            The HTTP status code of the response
        """
        business_metric_token_value = business_metric_token.business_metric_token
        return self._delete(f"business_metrics/{business_metric_token_value}")

    def update_business_metric(
        self, business_metric_token: BusinessMetricTokenParams, business_metric_update: CreateBusinessMetric
    ) -> BusinessMetric:
        """
        Update a specific business metric - PUT /business_metrics/{business_metric_token}

        Args:
            business_metric_token: The token of the business metric to update
            business_metric_update: The updated business metric object

        Returns:
            The updated business metric object
        """
        business_metric_token_value = business_metric_token.business_metric_token
        data = self._put(f"business_metrics/{business_metric_token_value}", business_metric_update)
        return BusinessMetric.model_validate(data)

    def get_business_metric_values(
        self,
        business_metric_token_values: BusinessMetricsBusinessMetricTokenValuesGetParametersQuery,
        business_metric_token_params: BusinessMetricTokenParams,
    ) -> BusinessMetricValues:
        """
        Get the values of a specific business metric - GET /business_metrics/{business_metric_token}/values

        Args:
            business_metric_token_values: The parameters to filter the business metric values
            business_metric_token_params: The token of the business metric to retrieve values for

        Returns:
            A dictionary containing the values of the business metric
        """
        business_metric_token_value = business_metric_token_params.business_metric_token
        paginated_data = self._get_paginated(
            f"business_metrics/{business_metric_token_value}/values", business_metric_token_values
        )
        return BusinessMetricValues.model_validate(paginated_data)

    # ---- Integration APIs ----

    def get_all_integrations(self, query_params: IntegrationsGetParametersQuery | None = None) -> Integrations:
        """
        Get all integrations - GET /integrations

        Args:
            query_params: Optional query parameters for filtering integrations

        Returns:
            An Integrations object which is a list of Integration objects
        """
        paginated_data = self._get_paginated("integrations", query_params)
        return Integrations.model_validate(paginated_data)

    def create_azure_integration(self, new_azure_integration: CreateAzureIntegration) -> Integration:
        """
        Create a new Azure integration - POST /integrations/azure

        Args:
            new_azure_integration: The new Azure integration object to create

        Returns:
            The created integration object
        """
        data = self._post("integrations/azure", new_azure_integration)
        return Integration.model_validate(data)

    def create_gcp_integration(self, new_gcp_integration: CreateGCPIntegration) -> Integration:
        """
        Create a new GCP integration - POST /integrations/gcp

        Args:
            new_gcp_integration: The new GCP integration object to create

        Returns:
            The created integration object
        """
        data = self._post("integrations/gcp", new_gcp_integration)
        return Integration.model_validate(data)

    def create_custom_provider_integration(
        self, new_custom_provider_integration: CreateCustomProviderIntegration
    ) -> Integration:
        """
        Create a new Custom Provider integration - POST /integrations/custom_provider

        Args:
            new_custom_provider_integration: The new custom provider integration object to create

        Returns:
            The created integration object
        """
        data = self._post("integrations/custom_provider", new_custom_provider_integration)
        return Integration.model_validate(data)

    def get_integration(self, integration_token_params: IntegrationTokenParams) -> Integration:
        """
        Retrieve a specific integration - GET /integrations/{integration_token}

        Args:
            integration_token_params: The token of the integration to retrieve, begins with 'intg_'

        Returns:
            The integration object
        """
        integration_token = integration_token_params.integration_token
        data = self._get(f"integrations/{integration_token}")
        return Integration.model_validate(data)

    def update_integration(
        self, integration_token_params: IntegrationTokenParams, workspace_tokens: Sequence[str]
    ) -> Integration:
        """
        Update a specific integration - PUT /integrations/{integration_token}

        Args:
            integration_token_params: The token of the integration to update, begins with 'intg_'
            workspace_tokens: Array of workspace tokens to associate with the integration

        Returns:
            The updated integration object
        """
        integration_token = integration_token_params.integration_token
        data = self._put(
            f"integrations/{integration_token}", IntegrationsIntegrationTokenPutRequest(root=workspace_tokens)
        )
        return Integration.model_validate(data)

    def delete_integration(self, integration_token_params: IntegrationTokenParams) -> HttpStatusCode:
        """
        Delete a specific integration - DELETE /integrations/{integration_token}

        Args:
            integration_token_params: The token of the integration to delete, begins with 'intg_'

        Returns:
            The HTTP status code of the response
        """
        integration_token = integration_token_params.integration_token
        return self._delete(f"integrations/{integration_token}")

    def get_integration_costs(self, integration_token_params: IntegrationTokenParams) -> UserCostsUploads:
        """
        List UserCostsUploads for an integration - GET /integrations/{integration_token}/costs

        Args:
            integration_token_params: The token of the integration, begins with 'intg_'

        Returns:
            A UserCostsUploads object containing a list of UserCostsUpload objects
        """
        integration_token = integration_token_params.integration_token
        data = self._get(f"integrations/{integration_token}/costs")
        return UserCostsUploads.model_validate(data)

    def delete_integration_costs(
        self,
        integration_token_params: IntegrationTokenParams,
        user_costs_upload_token: str,
    ) -> HttpStatusCode:
        """
        Delete a UserCostsUpload - DELETE /integrations/{integration_token}/costs/{user_costs_upload_token}

        Args:
            integration_token_params: The token of the integration, begins with 'intg_'
            user_costs_upload_token: The token of the user costs upload to delete

        Returns:
            The HTTP status code of the response
        """
        integration_token = integration_token_params.integration_token
        return self._delete(f"integrations/{integration_token}/costs/{user_costs_upload_token}")

    def upload_integration_costs(
        self,
        integration_token_params: IntegrationTokenParams,
        csv_data: bytes,
    ) -> dict:
        """
        Create UserCostsUpload via CSV for a Custom Provider Integration.

        POST /integrations/{integration_token}/costs.csv

        Args:
            integration_token_params: The token of the integration, begins with 'intg_'
            csv_data: CSV file data containing custom costs

        Returns:
            The response data from the server

        Note:
            This function doesn't use the _post protected method because we need to send
            form data with the CSV file rather than JSON data.
        """
        integration_token = integration_token_params.integration_token
        url = urljoin(self.base_url, f"integrations/{integration_token}/costs.csv")

        # Create the form data with the CSV file
        files = {"csv": ("costs.csv", csv_data, "text/csv")}

        # Send the request
        response = self.session.post(url, files=files, headers=self.session.headers, timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    # ---- Access Grants APIs ----

    def get_all_access_grants(self) -> AccessGrants:
        """
        Get all access grants - GET /access_grants

        Returns:
            An AccessGrants object which is a list of AccessGrant objects
        """
        paginated_data = self._get_paginated("access_grants")
        return AccessGrants.model_validate(paginated_data)

    def get_access_grant(self, access_grant_token_params: AccessGrantTokenParams) -> AccessGrant:
        """
        Retrieve a specific access grant - GET /access_grants/{access_grant_token}

        Args:
            access_grant_token_params: The token of the access grant to retrieve

        Returns:
            The access grant object
        """
        access_grant_token = access_grant_token_params.access_grant_token
        data = self._get(f"access_grants/{access_grant_token}")
        return AccessGrant.model_validate(data)

    def create_access_grant(self, new_access_grant: CreateAccessGrant) -> AccessGrant:
        """
        Create a new access grant - POST /access_grants

        Args:
            new_access_grant: The new access grant object to create

        Returns:
            The created access grant object
        """
        data = self._post("access_grants", new_access_grant)
        return AccessGrant.model_validate(data)

    def update_access_grant(
        self, access_grant_token_params: AccessGrantTokenParams, access_grant_update: UpdateAccessGrant
    ) -> AccessGrant:
        """
        Update a specific access grant - PUT /access_grants/{access_grant_token}

        Args:
            access_grant_token_params: The token of the access grant to update
            access_grant_update: The updated access grant object

        Returns:
            The updated access grant object
        """
        access_grant_token = access_grant_token_params.access_grant_token
        data = self._put(f"access_grants/{access_grant_token}", access_grant_update)
        return AccessGrant.model_validate(data)

    def delete_access_grant(self, access_grant_token_params: AccessGrantTokenParams) -> HttpStatusCode:
        """
        Delete a specific access grant - DELETE /access_grants/{access_grant_token}

        Args:
            access_grant_token_params: The token of the access grant to delete

        Returns:
            The HTTP status code of the response
        """
        access_grant_token = access_grant_token_params.access_grant_token
        return self._delete(f"access_grants/{access_grant_token}")

    # ---- Me API ----

    def get_me(self) -> Me:
        """
        Get information about the authenticated BearerToken - GET /me

        Returns:
            A Me object containing information about the authenticated user's token and workspaces
        """
        data = self._get("me")
        return Me.model_validate(data)

    # ---- Teams APIs ----

    def get_all_teams(self) -> Teams:
        """
        Get all teams - GET /teams

        Returns:
            A Teams object which is a list of Team objects
        """
        paginated_data = self._get_paginated("teams")
        return Teams.model_validate(paginated_data)

    def get_team(self, team_token_params: TeamTokenParams) -> Team:
        """
        Retrieve a specific team - GET /teams/{team_token}

        Args:
            team_token_params: The token of the team to retrieve

        Returns:
            The team object
        """
        team_token = team_token_params.team_token
        data = self._get(f"teams/{team_token}")
        return Team.model_validate(data)

    def create_team(self, new_team: CreateTeam) -> Team:
        """
        Create a new team - POST /teams

        Args:
            new_team: The new team object to create

        Returns:
            The created team object
        """
        data = self._post("teams", new_team)
        return Team.model_validate(data)

    def update_team(self, team_token_params: TeamTokenParams, team_update: UpdateTeam) -> Team:
        """
        Update a specific team - PUT /teams/{team_token}

        Args:
            team_token_params: The token of the team to update
            team_update: The updated team object

        Returns:
            The updated team object
        """
        team_token = team_token_params.team_token
        data = self._put(f"teams/{team_token}", team_update)
        return Team.model_validate(data)

    def delete_team(self, team_token_params: TeamTokenParams) -> HttpStatusCode:
        """
        Delete a specific team - DELETE /teams/{team_token}

        Args:
            team_token_params: The token of the team to delete

        Returns:
            The HTTP status code of the response
        """
        team_token = team_token_params.team_token
        return self._delete(f"teams/{team_token}")

    # ---- Anomaly Alerts & Notifications APIs ----

    def get_all_anomaly_alerts(
        self, anomaly_alerts_params: AnomalyAlertsGetParametersQuery | None = None
    ) -> AnomalyAlerts:
        """
        Get all anomaly alerts - GET /anomaly_alerts

        Args:
            anomaly_alerts_params: Optional query parameters for filtering anomaly alerts

        Returns:
            An AnomalyAlerts object which is a list of AnomalyAlert objects
        """
        paginated_data = self._get_paginated("anomaly_alerts", anomaly_alerts_params)
        return AnomalyAlerts.model_validate(paginated_data)

    def get_anomaly_alert(self, anomaly_alert_token_params: AnomalyAlertTokenParams) -> AnomalyAlert:
        """
        Retrieve a specific anomaly alert - GET /anomaly_alerts/{anomaly_alert_token}

        Args:
            anomaly_alert_token_params: The token of the anomaly alert to retrieve

        Returns:
            The anomaly alert object
        """
        anomaly_alert_token = anomaly_alert_token_params.anomaly_alert_token
        data = self._get(f"anomaly_alerts/{anomaly_alert_token}")
        return AnomalyAlert.model_validate(data)

    def update_anomaly_alert(
        self, anomaly_alert_token_params: AnomalyAlertTokenParams, anomaly_alert_update: UpdateAnomalyAlert
    ) -> AnomalyAlert:
        """
        Update a specific anomaly alert - PUT /anomaly_alerts/{anomaly_alert_token}

        Args:
            anomaly_alert_token_params: The token of the anomaly alert to update
            anomaly_alert_update: The updated anomaly alert object

        Returns:
            The updated anomaly alert object
        """
        anomaly_alert_token = anomaly_alert_token_params.anomaly_alert_token
        data = self._put(f"anomaly_alerts/{anomaly_alert_token}", anomaly_alert_update)
        return AnomalyAlert.model_validate(data)

    def get_all_anomaly_notifications(self) -> AnomalyNotifications:
        """
        Get all anomaly notifications - GET /anomaly_notifications

        Returns:
            An AnomalyNotifications object which is a list of AnomalyNotification objects
        """
        paginated_data = self._get_paginated("anomaly_notifications")
        return AnomalyNotifications.model_validate(paginated_data)

    def get_anomaly_notification(
        self, anomaly_notification_token_params: AnomalyNotificationTokenParams
    ) -> AnomalyNotification:
        """
        Retrieve a specific anomaly notification - GET /anomaly_notifications/{anomaly_notification_token}

        Args:
            anomaly_notification_token_params: The token of the anomaly notification to retrieve

        Returns:
            The anomaly notification object
        """
        anomaly_notification_token = anomaly_notification_token_params.anomaly_notification_token
        data = self._get(f"anomaly_notifications/{anomaly_notification_token}")
        return AnomalyNotification.model_validate(data)

    def create_anomaly_notification(self, new_anomaly_notification: CreateAnomalyNotification) -> AnomalyNotification:
        """
        Create a new anomaly notification - POST /anomaly_notifications

        Args:
            new_anomaly_notification: The new anomaly notification object to create

        Returns:
            The created anomaly notification object
        """
        data = self._post("anomaly_notifications", new_anomaly_notification)
        return AnomalyNotification.model_validate(data)

    def update_anomaly_notification(
        self,
        anomaly_notification_token_params: AnomalyNotificationTokenParams,
        anomaly_notification_update: UpdateAnomalyNotification,
    ) -> AnomalyNotification:
        """
        Update a specific anomaly notification - PUT /anomaly_notifications/{anomaly_notification_token}

        Args:
            anomaly_notification_token_params: The token of the anomaly notification to update
            anomaly_notification_update: The updated anomaly notification object

        Returns:
            The updated anomaly notification object
        """
        anomaly_notification_token = anomaly_notification_token_params.anomaly_notification_token
        data = self._put(f"anomaly_notifications/{anomaly_notification_token}", anomaly_notification_update)
        return AnomalyNotification.model_validate(data)

    def delete_anomaly_notification(
        self, anomaly_notification_token_params: AnomalyNotificationTokenParams
    ) -> HttpStatusCode:
        """
        Delete a specific anomaly notification - DELETE /anomaly_notifications/{anomaly_notification_token}

        Args:
            anomaly_notification_token_params: The token of the anomaly notification to delete

        Returns:
            The HTTP status code of the response
        """
        anomaly_notification_token = anomaly_notification_token_params.anomaly_notification_token
        return self._delete(f"anomaly_notifications/{anomaly_notification_token}")

    # ---- Billing Rules APIs ----

    def get_all_billing_rules(self) -> BillingRules:
        """
        Get all billing rules - GET /billing_rules

        Returns:
            A BillingRules object which is a list of BillingRule objects
        """
        paginated_data = self._get_paginated("billing_rules")
        return BillingRules.model_validate(paginated_data)

    def get_billing_rule(self, billing_rule_token_params: BillingRuleTokenParams) -> BillingRule:
        """
        Retrieve a specific billing rule - GET /billing_rules/{billing_rule_token}

        Args:
            billing_rule_token_params: The token of the billing rule to retrieve

        Returns:
            The billing rule object
        """
        billing_rule_token = billing_rule_token_params.billing_rule_token
        data = self._get(f"billing_rules/{billing_rule_token}")
        return BillingRule.model_validate(data)

    def create_billing_rule(self, new_billing_rule: CreateBillingRule) -> BillingRule:
        """
        Create a new billing rule - POST /billing_rules

        Args:
            new_billing_rule: The new billing rule object to create

        Returns:
            The created billing rule object
        """
        data = self._post("billing_rules", new_billing_rule)
        return BillingRule.model_validate(data)

    def update_billing_rule(
        self, billing_rule_token_params: BillingRuleTokenParams, billing_rule_update: UpdateBillingRule
    ) -> BillingRule:
        """
        Update a specific billing rule - PUT /billing_rules/{billing_rule_token}

        Args:
            billing_rule_token_params: The token of the billing rule to update
            billing_rule_update: The updated billing rule object

        Returns:
            The updated billing rule object
        """
        billing_rule_token = billing_rule_token_params.billing_rule_token
        data = self._put(f"billing_rules/{billing_rule_token}", billing_rule_update)
        return BillingRule.model_validate(data)

    def delete_billing_rule(self, billing_rule_token_params: BillingRuleTokenParams) -> HttpStatusCode:
        """
        Delete a specific billing rule - DELETE /billing_rules/{billing_rule_token}

        Args:
            billing_rule_token_params: The token of the billing rule to delete

        Returns:
            The HTTP status code of the response
        """
        billing_rule_token = billing_rule_token_params.billing_rule_token
        return self._delete(f"billing_rules/{billing_rule_token}")

    # ---- Budgets APIs ----

    def get_all_budgets(self) -> Budgets:
        """
        Get all budgets - GET /budgets

        Returns:
            A Budgets object which is a list of Budget objects
        """
        paginated_data = self._get_paginated("budgets")
        return Budgets.model_validate(paginated_data)

    def get_budget(
        self, budget_token_params: BudgetTokenParams, budget_params: BudgetsBudgetTokenGetParametersQuery | None = None
    ) -> Budget:
        """
        Retrieve a specific budget - GET /budgets/{budget_token}

        Args:
            budget_token_params: The token of the budget to retrieve
            budget_params: Optional query parameters for the budget

        Returns:
            The budget object
        """
        budget_token = budget_token_params.budget_token
        data = self._get(f"budgets/{budget_token}", budget_params)
        return Budget.model_validate(data)

    def create_budget(self, new_budget: CreateBudget) -> Budget:
        """
        Create a new budget - POST /budgets

        Args:
            new_budget: The new budget object to create

        Returns:
            The created budget object
        """
        data = self._post("budgets", new_budget)
        return Budget.model_validate(data)

    def update_budget(self, budget_token_params: BudgetTokenParams, budget_update: UpdateBudget) -> Budget:
        """
        Update a specific budget - PUT /budgets/{budget_token}

        Args:
            budget_token_params: The token of the budget to update
            budget_update: The updated budget object

        Returns:
            The updated budget object
        """
        budget_token = budget_token_params.budget_token
        data = self._put(f"budgets/{budget_token}", budget_update)
        return Budget.model_validate(data)

    def delete_budget(self, budget_token_params: BudgetTokenParams) -> HttpStatusCode:
        """
        Delete a specific budget - DELETE /budgets/{budget_token}

        Args:
            budget_token_params: The token of the budget to delete

        Returns:
            The HTTP status code of the response
        """
        budget_token = budget_token_params.budget_token
        return self._delete(f"budgets/{budget_token}")

    # ---- Budget Alerts APIs ----

    def get_all_budget_alerts(self) -> BudgetAlerts:
        """
        Get all budget alerts - GET /budget_alerts

        Returns:
            A BudgetAlerts object which is a list of BudgetAlert objects
        """
        paginated_data = self._get_paginated("budget_alerts")
        return BudgetAlerts.model_validate(paginated_data)

    def get_budget_alert(self, budget_alert_token_params: BudgetAlertTokenParams) -> BudgetAlert:
        """
        Retrieve a specific budget alert - GET /budget_alerts/{budget_alert_token}

        Args:
            budget_alert_token_params: The token of the budget alert to retrieve

        Returns:
            The budget alert object
        """
        budget_alert_token = budget_alert_token_params.budget_alert_token
        data = self._get(f"budget_alerts/{budget_alert_token}")
        return BudgetAlert.model_validate(data)

    def create_budget_alert(self, new_budget_alert: BudgetAlertsPostRequest) -> BudgetAlert:
        """
        Create a new budget alert - POST /budget_alerts

        Args:
            new_budget_alert: The new budget alert object to create

        Returns:
            The created budget alert object
        """
        data = self._post("budget_alerts", new_budget_alert)
        return BudgetAlert.model_validate(data)

    def update_budget_alert(
        self,
        budget_alert_token_params: BudgetAlertTokenParams,
        budget_alert_update: BudgetAlertsBudgetAlertTokenPutRequest,
    ) -> BudgetAlert:
        """
        Update a specific budget alert - PUT /budget_alerts/{budget_alert_token}

        Args:
            budget_alert_token_params: The token of the budget alert to update
            budget_alert_update: The updated budget alert object

        Returns:
            The updated budget alert object
        """
        budget_alert_token = budget_alert_token_params.budget_alert_token
        data = self._put(f"budget_alerts/{budget_alert_token}", budget_alert_update)
        return BudgetAlert.model_validate(data)

    def delete_budget_alert(self, budget_alert_token_params: BudgetAlertTokenParams) -> HttpStatusCode:
        """
        Delete a specific budget alert - DELETE /budget_alerts/{budget_alert_token}

        Args:
            budget_alert_token_params: The token of the budget alert to delete

        Returns:
            The HTTP status code of the response
        """
        budget_alert_token = budget_alert_token_params.budget_alert_token
        return self._delete(f"budget_alerts/{budget_alert_token}")

    # ---- Cost Alerts APIs ----

    def get_all_cost_alerts(self) -> CostAlerts:
        """
        Get all cost alerts - GET /cost_alerts

        Returns:
            A CostAlerts object which is a list of CostAlert objects
        """
        paginated_data = self._get_paginated("cost_alerts")
        return CostAlerts.model_validate(paginated_data)

    def get_cost_alert(self, cost_alert_token_params: CostAlertTokenParams) -> CostAlert:
        """
        Retrieve a specific cost alert - GET /cost_alerts/{cost_alert_token}

        Args:
            cost_alert_token_params: The token of the cost alert to retrieve

        Returns:
            The cost alert object
        """
        cost_alert_token = cost_alert_token_params.cost_alert_token
        data = self._get(f"cost_alerts/{cost_alert_token}")
        return CostAlert.model_validate(data)

    def get_cost_alert_events(
        self,
        cost_alert_token_params: CostAlertTokenParams,
        query_params: CostAlertsCostAlertTokenEventsGetParametersQuery | None = None,
    ) -> CostAlertEvents:
        """
        Get events for a specific cost alert - GET /cost_alerts/{cost_alert_token}/events

        Args:
            cost_alert_token_params: The token of the cost alert
            query_params: Optional query parameters for filtering events

        Returns:
            A CostAlertEvents object containing the events
        """
        cost_alert_token = cost_alert_token_params.cost_alert_token
        paginated_data = self._get_paginated(f"cost_alerts/{cost_alert_token}/events", query_params)
        return CostAlertEvents.model_validate(paginated_data)

    def get_cost_alert_event(
        self, cost_alert_token_params: CostAlertTokenParams, cost_alert_event_token_params: CostAlertEventTokenParams
    ) -> CostAlertEvent:
        """
        Retrieve a specific cost alert event - GET /cost_alerts/{cost_alert_token}/events/{event_token}

        Args:
            cost_alert_token_params: The token of the cost alert
            cost_alert_event_token_params: The token of the event to retrieve

        Returns:
            The cost alert event object
        """
        cost_alert_token = cost_alert_token_params.cost_alert_token
        event_token = cost_alert_event_token_params.event_token
        data = self._get(f"cost_alerts/{cost_alert_token}/events/{event_token}")
        return CostAlertEvent.model_validate(data)

    def create_cost_alert(self, new_cost_alert: CreateCostAlert) -> CostAlert:
        """
        Create a new cost alert - POST /cost_alerts

        Args:
            new_cost_alert: The new cost alert object to create

        Returns:
            The created cost alert object
        """
        data = self._post("cost_alerts", new_cost_alert)
        return CostAlert.model_validate(data)

    def update_cost_alert(
        self, cost_alert_token_params: CostAlertTokenParams, cost_alert_update: UpdateCostAlert
    ) -> CostAlert:
        """
        Update a specific cost alert - PUT /cost_alerts/{cost_alert_token}

        Args:
            cost_alert_token_params: The token of the cost alert to update
            cost_alert_update: The updated cost alert object

        Returns:
            The updated cost alert object
        """
        cost_alert_token = cost_alert_token_params.cost_alert_token
        data = self._put(f"cost_alerts/{cost_alert_token}", cost_alert_update)
        return CostAlert.model_validate(data)

    def delete_cost_alert(self, cost_alert_token_params: CostAlertTokenParams) -> HttpStatusCode:
        """
        Delete a specific cost alert - DELETE /cost_alerts/{cost_alert_token}

        Args:
            cost_alert_token_params: The token of the cost alert to delete

        Returns:
            The HTTP status code of the response
        """
        cost_alert_token = cost_alert_token_params.cost_alert_token
        return self._delete(f"cost_alerts/{cost_alert_token}")

    # ---- Cost Reports - Forecasted Costs API ----

    def get_cost_report_forecasted_costs(
        self,
        cost_report_token_params: CostReportTokenParams,
        query_params: CostReportsCostReportTokenForecastedCostsGetParametersQuery | None = None,
    ) -> ForecastedCosts:
        """
        Get forecasted costs for a cost report - GET /cost_reports/{cost_report_token}/forecasted_costs

        Args:
            cost_report_token_params: The token of the cost report
            query_params: Optional query parameters for filtering forecasted costs

        Returns:
            A ForecastedCosts object containing the forecasted costs
        """
        cost_report_token = cost_report_token_params.cost_report_token
        paginated_data = self._get_paginated(f"cost_reports/{cost_report_token}/forecasted_costs", query_params)
        return ForecastedCosts.model_validate(paginated_data)

    # ---- Cost Providers & Services APIs ----

    def get_cost_providers(self, workspace_token_params: WorkspaceTokenParams | None = None) -> CostProviders:
        """
        Get all cost providers - GET /cost_providers

        Args:
            workspace_token_params: Optional workspace token parameters

        Returns:
            A CostProviders object which is a list of CostProvider objects
        """
        data = self._get("cost_providers", workspace_token_params)
        return CostProviders.model_validate(data)

    def get_cost_services(self, workspace_token_params: WorkspaceTokenParams | None = None) -> CostServices:
        """
        Get all cost services - GET /cost_services

        Args:
            workspace_token_params: Optional workspace token parameters

        Returns:
            A CostServices object which is a list of CostService objects
        """
        data = self._get("cost_services", workspace_token_params)
        return CostServices.model_validate(data)

    # ---- Dashboards APIs ----

    def get_all_dashboards(self, workspace_token_params: DashboardsGetParametersQuery | None = None) -> Dashboards:
        """
        Get all dashboards - GET /dashboards

        Args:
            workspace_token_params: Optional workspace token parameters

        Returns:
            A Dashboards object containing all dashboards
        """
        paginated_data = self._get_paginated("dashboards", workspace_token_params)
        return Dashboards.model_validate(paginated_data)

    def get_dashboard(self, dashboard_token_params: DashboardTokenParams) -> Dashboard:
        """
        Get a single dashboard - GET /dashboards/{dashboard_token}

        Args:
            dashboard_token_params: The token of the dashboard to retrieve

        Returns:
            A Dashboard object
        """
        dashboard_token = dashboard_token_params.dashboard_token
        data = self._get(f"dashboards/{dashboard_token}")
        return Dashboard.model_validate(data)

    def create_dashboard(self, new_dashboard: CreateDashboard) -> Dashboard:
        """
        Create a new dashboard - POST /dashboards

        Args:
            new_dashboard: The dashboard configuration to create

        Returns:
            The created Dashboard object
        """
        data = self._post("dashboards", new_dashboard)
        return Dashboard.model_validate(data)

    def update_dashboard(
        self, dashboard_token_params: DashboardTokenParams, dashboard_update: UpdateDashboard
    ) -> Dashboard:
        """
        Update an existing dashboard - PUT /dashboards/{dashboard_token}

        Args:
            dashboard_token_params: The token of the dashboard to update
            dashboard_update: The updated dashboard configuration

        Returns:
            The updated Dashboard object
        """
        dashboard_token = dashboard_token_params.dashboard_token
        data = self._put(f"dashboards/{dashboard_token}", dashboard_update)
        return Dashboard.model_validate(data)

    def delete_dashboard(self, dashboard_token_params: DashboardTokenParams) -> HttpStatusCode:
        """
        Delete a dashboard - DELETE /dashboards/{dashboard_token}

        Args:
            dashboard_token_params: The token of the dashboard to delete

        Returns:
            HTTP 204 No Content on successful deletion
        """
        dashboard_token = dashboard_token_params.dashboard_token
        return self._delete(f"dashboards/{dashboard_token}")

    # ---- OpenAPI Specification ----

    def get_openapi_spec(self) -> dict:
        """
        Get the OpenAPI 3 specification - GET /oas_v3.json

        Returns:
            The OpenAPI specification as a dictionary
        """
        return self._get("oas_v3.json")

    # ---- Products & Pricing APIs ----

    def get_all_products(self) -> Products:
        """
        Get all products - GET /products

        Returns:
            A Products object which is a list of Product objects
        """
        paginated_data = self._get_paginated("products")
        return Products.model_validate(paginated_data)

    def get_product(self, product_id_params: ProductIdParams) -> Product:
        """
        Retrieve a specific product - GET /products/{id}

        Args:
            product_id_params: The ID of the product to retrieve

        Returns:
            The product object
        """
        product_id = product_id_params.id
        data = self._get(f"products/{product_id}")
        return Product.model_validate(data)

    def get_product_prices(self, product_id_params: ProductIdParams) -> Prices:
        """
        Get all prices for a product - GET /products/{product_id}/prices

        Args:
            product_id_params: The ID of the product to retrieve prices for

        Returns:
            A Prices object which is a list of Price objects
        """
        product_id = product_id_params.id
        paginated_data = self._get_paginated(f"products/{product_id}/prices")
        return Prices.model_validate(paginated_data)

    def get_product_price(self, product_id_params: ProductIdParams, price_id_params: ProductPriceIdParams) -> Price:
        """
        Retrieve a specific price for a product - GET /products/{product_id}/prices/{id}

        Args:
            product_id_params: The ID of the product
            price_id_params: The ID of the price to retrieve

        Returns:
            The price object
        """
        product_id = product_id_params.id
        price_id = price_id_params.id
        data = self._get(f"products/{product_id}/prices/{price_id}")
        return Price.model_validate(data)

    # ---- Recommendations APIs ----

    def get_all_recommendations(self) -> Recommendations:
        """
        Get all recommendations - GET /recommendations

        Returns:
            A Recommendations object which is a list of Recommendation objects
        """
        paginated_data = self._get_paginated("recommendations")
        return Recommendations.model_validate(paginated_data)

    def get_recommendation(self, recommendation_token_params: RecommendationTokenParams) -> Recommendation:
        """
        Retrieve a specific recommendation - GET /recommendations/{recommendation_token}

        Args:
            recommendation_token_params: The token of the recommendation to retrieve

        Returns:
            The recommendation object
        """
        recommendation_token = recommendation_token_params.recommendation_token
        data = self._get(f"recommendations/{recommendation_token}")
        return Recommendation.model_validate(data)

    def get_recommendation_resources(
        self, recommendation_token_params: RecommendationTokenParams
    ) -> RecommendationResources:
        """
        Get resources for a recommendation - GET /recommendations/{recommendation_token}/resources

        Args:
            recommendation_token_params: The token of the recommendation to retrieve resources for

        Returns:
            A RecommendationResources object which is a list of RecommendationResource objects
        """
        recommendation_token = recommendation_token_params.recommendation_token
        paginated_data = self._get_paginated(f"recommendations/{recommendation_token}/resources")
        return RecommendationResources.model_validate(paginated_data)

    def get_recommendation_resource(
        self,
        recommendation_token_params: RecommendationTokenParams,
        recommendation_resource_token_params: RecommendationResourceTokenParams,
    ) -> RecommendationResource:
        """
        Retrieve a specific recommendation resource.

        GET /recommendations/{recommendation_token}/resources/{resource_token}

        Args:
            recommendation_token_params: The token of the recommendation
            recommendation_resource_token_params: The token of the recommendation resource to retrieve

        Returns:
            The recommendation resource object
        """
        recommendation_token = recommendation_token_params.recommendation_token
        resource_token = recommendation_resource_token_params.resource_token
        data = self._get(f"recommendations/{recommendation_token}/resources/{resource_token}")
        return RecommendationResource.model_validate(data)

    # ---- Report Notifications APIs ----

    def get_all_report_notifications(self) -> ReportNotifications:
        """
        Get all report notifications - GET /report_notifications

        Returns:
            A ReportNotifications object which is a list of ReportNotification objects
        """
        paginated_data = self._get_paginated("report_notifications")
        return ReportNotifications.model_validate(paginated_data)

    def get_report_notification(
        self, report_notification_token_params: ReportNotificationTokenParams
    ) -> ReportNotification:
        """
        Retrieve a specific report notification - GET /report_notifications/{report_notification_token}

        Args:
            report_notification_token_params: The token of the report notification to retrieve

        Returns:
            The report notification object
        """
        report_notification_token = report_notification_token_params.report_notification_token
        data = self._get(f"report_notifications/{report_notification_token}")
        return ReportNotification.model_validate(data)

    def create_report_notification(self, new_report_notification: CreateReportNotification) -> ReportNotification:
        """
        Create a new report notification - POST /report_notifications

        Args:
            new_report_notification: The new report notification object to create

        Returns:
            The created report notification object
        """
        data = self._post("report_notifications", new_report_notification)
        return ReportNotification.model_validate(data)

    def update_report_notification(
        self,
        report_notification_token_params: ReportNotificationTokenParams,
        report_notification_update: UpdateReportNotification,
    ) -> ReportNotification:
        """
        Update a specific report notification - PUT /report_notifications/{report_notification_token}

        Args:
            report_notification_token_params: The token of the report notification to update
            report_notification_update: The updated report notification object

        Returns:
            The updated report notification object
        """
        report_notification_token = report_notification_token_params.report_notification_token
        data = self._put(f"report_notifications/{report_notification_token}", report_notification_update)
        return ReportNotification.model_validate(data)

    def delete_report_notification(
        self, report_notification_token_params: ReportNotificationTokenParams
    ) -> HttpStatusCode:
        """
        Delete a specific report notification - DELETE /report_notifications/{report_notification_token}

        Args:
            report_notification_token_params: The token of the report notification to delete

        Returns:
            The HTTP status code of the response
        """
        report_notification_token = report_notification_token_params.report_notification_token
        return self._delete(f"report_notifications/{report_notification_token}")

    # ---- Resource Reports APIs ----

    def get_all_resource_reports(self) -> ResourceReports:
        """
        Get all resource reports - GET /resource_reports

        Returns:
            A ResourceReports object which is a list of ResourceReport objects
        """
        paginated_data = self._get_paginated("resource_reports")
        return ResourceReports.model_validate(paginated_data)

    def get_resource_report(self, resource_report_token_params: ResourceReportTokenParams) -> ResourceReport:
        """
        Retrieve a specific resource report - GET /resource_reports/{resource_report_token}

        Args:
            resource_report_token_params: The token of the resource report to retrieve

        Returns:
            The resource report object
        """
        token_value = resource_report_token_params.resource_report_token
        data = self._get(f"resource_reports/{token_value}")
        return ResourceReport.model_validate(data)

    def create_resource_report(self, new_resource_report: CreateResourceReport) -> ResourceReport:
        """
        Create a new resource report - POST /resource_reports

        Args:
            new_resource_report: The new resource report object to create

        Returns:
            The created resource report object
        """
        data = self._post("resource_reports", new_resource_report)
        return ResourceReport.model_validate(data)

    def update_resource_report(
        self,
        resource_report_token_params: ResourceReportTokenParams,
        resource_report_update: UpdateResourceReport,
    ) -> ResourceReport:
        """
        Update a specific resource report - PUT /resource_reports/{resource_report_token}

        Args:
            resource_report_token_params: The token of the resource report to update
            resource_report_update: The updated resource report object

        Returns:
            The updated resource report object
        """
        token_value = resource_report_token_params.resource_report_token
        data = self._put(f"resource_reports/{token_value}", resource_report_update)
        return ResourceReport.model_validate(data)

    def delete_resource_report(self, resource_report_token_params: ResourceReportTokenParams) -> HttpStatusCode:
        """
        Delete a specific resource report - DELETE /resource_reports/{resource_report_token}

        Args:
            resource_report_token_params: The token of the resource report to delete

        Returns:
            The HTTP status code of the response
        """
        token_value = resource_report_token_params.resource_report_token
        return self._delete(f"resource_reports/{token_value}")

    # ---- Resources APIs ----

    def get_all_resources(self, query_params: ResourcesGetParametersQuery) -> Resources:
        """
        Get all resources - GET /resources

        Args:
            query_params: Query parameters for filtering resources, must include resource_report_token

        Returns:
            A Resources object which is a list of Resource objects
        """
        data = self._get("resources", query_params)
        return Resources.model_validate(data)

    def get_resource(self, resource_token_params: ResourceTokenParams) -> Resource:
        """
        Retrieve a specific resource - GET /resources/{resource_token}

        Args:
            resource_token_params: The token of the resource to retrieve

        Returns:
            The resource object
        """
        token_value = resource_token_params.resource_token
        data = self._get(f"resources/{token_value}")
        return Resource.model_validate(data)

    # ---- Segments APIs ----

    def get_all_segments(self) -> Segments:
        """
        Get all segments - GET /segments

        Returns:
            A Segments object which is a list of Segment objects
        """
        paginated_data = self._get_paginated("segments")
        return Segments.model_validate(paginated_data)

    def get_segment(self, segment_token_params: SegmentTokenParams) -> Segment:
        """
        Retrieve a specific segment - GET /segments/{segment_token}

        Args:
            segment_token_params: The token of the segment to retrieve

        Returns:
            The segment object
        """
        token_value = segment_token_params.segment_token
        data = self._get(f"segments/{token_value}")
        return Segment.model_validate(data)

    def create_segment(self, new_segment: CreateSegment) -> Segment:
        """
        Create a new segment - POST /segments

        Args:
            new_segment: The new segment object to create

        Returns:
            The created segment object
        """
        data = self._post("segments", new_segment)
        return Segment.model_validate(data)

    def update_segment(
        self,
        segment_token_params: SegmentTokenParams,
        segment_update: UpdateSegment,
    ) -> Segment:
        """
        Update a specific segment - PUT /segments/{segment_token}

        Args:
            segment_token_params: The token of the segment to update
            segment_update: The updated segment object

        Returns:
            The updated segment object
        """
        token_value = segment_token_params.segment_token
        data = self._put(f"segments/{token_value}", segment_update)
        return Segment.model_validate(data)

    def delete_segment(self, segment_token_params: SegmentTokenParams) -> HttpStatusCode:
        """
        Delete a specific segment - DELETE /segments/{segment_token}

        Args:
            segment_token_params: The token of the segment to delete

        Returns:
            The HTTP status code of the response
        """
        token_value = segment_token_params.segment_token
        return self._delete(f"segments/{token_value}")

    # ---- Kubernetes Efficiency Reports APIs ----

    def get_all_kubernetes_efficiency_reports(self) -> KubernetesEfficiencyReports:
        """
        Get all kubernetes efficiency reports - GET /kubernetes_efficiency_reports

        Returns:
            A KubernetesEfficiencyReports object which is a list of KubernetesEfficiencyReport objects
        """
        paginated_data = self._get_paginated("kubernetes_efficiency_reports")
        return KubernetesEfficiencyReports.model_validate(paginated_data)

    def get_kubernetes_efficiency_report(
        self, kubernetes_efficiency_report_token_params: KubernetesEfficiencyReportTokenParams
    ) -> KubernetesEfficiencyReport:
        """
        Retrieve a specific kubernetes efficiency report.

        GET /kubernetes_efficiency_reports/{kubernetes_efficiency_report_token}

        Args:
            kubernetes_efficiency_report_token_params: The token of the kubernetes efficiency report to retrieve

        Returns:
            The kubernetes efficiency report object
        """
        token_value = kubernetes_efficiency_report_token_params.kubernetes_efficiency_report_token
        data = self._get(f"kubernetes_efficiency_reports/{token_value}")
        return KubernetesEfficiencyReport.model_validate(data)

    def create_kubernetes_efficiency_report(
        self, new_kubernetes_efficiency_report: CreateKubernetesEfficiencyReport
    ) -> KubernetesEfficiencyReport:
        """
        Create a new kubernetes efficiency report - POST /kubernetes_efficiency_reports

        Args:
            new_kubernetes_efficiency_report: The new kubernetes efficiency report object to create

        Returns:
            The created kubernetes efficiency report object
        """
        data = self._post("kubernetes_efficiency_reports", new_kubernetes_efficiency_report)
        return KubernetesEfficiencyReport.model_validate(data)

    def update_kubernetes_efficiency_report(
        self,
        kubernetes_efficiency_report_token_params: KubernetesEfficiencyReportTokenParams,
        kubernetes_efficiency_report_update: UpdateKubernetesEfficiencyReport,
    ) -> KubernetesEfficiencyReport:
        """
        Update a specific kubernetes efficiency report.

        PUT /kubernetes_efficiency_reports/{kubernetes_efficiency_report_token}

        Args:
            kubernetes_efficiency_report_token_params: The token of the kubernetes efficiency report to update
            kubernetes_efficiency_report_update: The updated kubernetes efficiency report object

        Returns:
            The updated kubernetes efficiency report object
        """
        token_value = kubernetes_efficiency_report_token_params.kubernetes_efficiency_report_token
        data = self._put(f"kubernetes_efficiency_reports/{token_value}", kubernetes_efficiency_report_update)
        return KubernetesEfficiencyReport.model_validate(data)

    def delete_kubernetes_efficiency_report(
        self, kubernetes_efficiency_report_token_params: KubernetesEfficiencyReportTokenParams
    ) -> HttpStatusCode:
        """
        Delete a specific kubernetes efficiency report.

        DELETE /kubernetes_efficiency_reports/{kubernetes_efficiency_report_token}

        Args:
            kubernetes_efficiency_report_token_params: The token of the kubernetes efficiency report to delete

        Returns:
            The HTTP status code of the response
        """
        token_value = kubernetes_efficiency_report_token_params.kubernetes_efficiency_report_token
        return self._delete(f"kubernetes_efficiency_reports/{token_value}")

    # ---- Managed Accounts APIs ----

    def get_all_managed_accounts(self) -> ManagedAccounts:
        """
        Get all managed accounts - GET /managed_accounts

        Returns:
            A ManagedAccounts object which is a list of ManagedAccount objects
        """
        paginated_data = self._get_paginated("managed_accounts")
        return ManagedAccounts.model_validate(paginated_data)

    def get_managed_account(self, managed_account_token_params: ManagedAccountTokenParams) -> ManagedAccount:
        """
        Retrieve a specific managed account - GET /managed_accounts/{managed_account_token}

        Args:
            managed_account_token_params: The token of the managed account to retrieve

        Returns:
            The managed account object
        """
        token_value = managed_account_token_params.managed_account_token
        data = self._get(f"managed_accounts/{token_value}")
        return ManagedAccount.model_validate(data)

    def create_managed_account(self, new_managed_account: CreateManagedAccount) -> ManagedAccount:
        """
        Create a new managed account - POST /managed_accounts

        Args:
            new_managed_account: The new managed account object to create

        Returns:
            The created managed account object
        """
        data = self._post("managed_accounts", new_managed_account)
        return ManagedAccount.model_validate(data)

    def update_managed_account(
        self,
        managed_account_token_params: ManagedAccountTokenParams,
        managed_account_update: UpdateManagedAccount,
    ) -> ManagedAccount:
        """
        Update a specific managed account - PUT /managed_accounts/{managed_account_token}

        Args:
            managed_account_token_params: The token of the managed account to update
            managed_account_update: The updated managed account object

        Returns:
            The updated managed account object
        """
        token_value = managed_account_token_params.managed_account_token
        data = self._put(f"managed_accounts/{token_value}", managed_account_update)
        return ManagedAccount.model_validate(data)

    def delete_managed_account(self, managed_account_token_params: ManagedAccountTokenParams) -> HttpStatusCode:
        """
        Delete a specific managed account - DELETE /managed_accounts/{managed_account_token}

        Args:
            managed_account_token_params: The token of the managed account to delete

        Returns:
            The HTTP status code of the response
        """
        token_value = managed_account_token_params.managed_account_token
        return self._delete(f"managed_accounts/{token_value}")

    # ---- Network Flow Reports APIs ----

    def get_all_network_flow_reports(self) -> NetworkFlowReports:
        """
        Get all network flow reports - GET /network_flow_reports

        Returns:
            A NetworkFlowReports object which is a list of NetworkFlowReport objects
        """
        paginated_data = self._get_paginated("network_flow_reports")
        return NetworkFlowReports.model_validate(paginated_data)

    # ---- Tags APIs ----

    def get_all_tags(self, query_params: TagsGetParametersQuery | None = None) -> Tags:
        """
        Get all tags - GET /tags

        Args:
            query_params: Optional query parameters for filtering tags

        Returns:
            A Tags object which is a list of Tag objects
        """
        paginated_data = self._get_paginated("tags", query_params)
        return Tags.model_validate(paginated_data)

    def get_tag_values(
        self, tag_key_params: TagKeyParams, query_params: TagsKeyValuesGetParametersQuery | None = None
    ) -> TagValues:
        """
        Get all values for a tag key - GET /tags/{key}/values

        Args:
            tag_key_params: The key of the tag to retrieve values for
            query_params: Optional query parameters for filtering tag values

        Returns:
            A TagValues object which is a list of TagValue objects
        """
        key = tag_key_params.key
        paginated_data = self._get_paginated(f"tags/{key}/values", query_params)
        return TagValues.model_validate(paginated_data)

    def update_tags(self, tag_update: UpdateTag) -> Tag:
        """
        Update tags - PUT /tags

        Args:
            tag_update: The update tag object

        Returns:
            The updated Tag object
        """
        data = self._put("tags", tag_update)
        return Tag.model_validate(data)

    def get_network_flow_report(
        self, network_flow_report_token_params: NetworkFlowReportTokenParams
    ) -> NetworkFlowReport:
        """
        Retrieve a specific network flow report - GET /network_flow_reports/{network_flow_report_token}

        Args:
            network_flow_report_token_params: The token of the network flow report to retrieve

        Returns:
            The network flow report object
        """
        token_value = network_flow_report_token_params.network_flow_report_token
        data = self._get(f"network_flow_reports/{token_value}")
        return NetworkFlowReport.model_validate(data)

    def create_network_flow_report(self, new_network_flow_report: CreateNetworkFlowReport) -> NetworkFlowReport:
        """
        Create a new network flow report - POST /network_flow_reports

        Args:
            new_network_flow_report: The new network flow report object to create

        Returns:
            The created network flow report object
        """
        data = self._post("network_flow_reports", new_network_flow_report)
        return NetworkFlowReport.model_validate(data)

    def update_network_flow_report(
        self,
        network_flow_report_token_params: NetworkFlowReportTokenParams,
        network_flow_report_update: UpdateNetworkFlowReport,
    ) -> NetworkFlowReport:
        """
        Update a specific network flow report - PUT /network_flow_reports/{network_flow_report_token}

        Args:
            network_flow_report_token_params: The token of the network flow report to update
            network_flow_report_update: The updated network flow report object

        Returns:
            The updated network flow report object
        """
        token_value = network_flow_report_token_params.network_flow_report_token
        data = self._put(f"network_flow_reports/{token_value}", network_flow_report_update)
        return NetworkFlowReport.model_validate(data)

    def delete_network_flow_report(
        self, network_flow_report_token_params: NetworkFlowReportTokenParams
    ) -> HttpStatusCode:
        """
        Delete a specific network flow report - DELETE /network_flow_reports/{network_flow_report_token}

        Args:
            network_flow_report_token_params: The token of the network flow report to delete

        Returns:
            The HTTP status code of the response
        """
        token_value = network_flow_report_token_params.network_flow_report_token
        return self._delete(f"network_flow_reports/{token_value}")

    # ---- Financial Commitments & Reports APIs ----

    def get_all_financial_commitments(
        self, workspace_token_params: WorkspaceTokenParams | None = None
    ) -> FinancialCommitments:
        """
        Get all financial commitments - GET /financial_commitments

        Args:
            workspace_token_params: Optional workspace token parameters

        Returns:
            A FinancialCommitments object which is a list of FinancialCommitment objects
        """
        paginated_data = self._get_paginated("financial_commitments", workspace_token_params)
        return FinancialCommitments.model_validate(paginated_data)

    def get_all_financial_commitment_reports(self) -> FinancialCommitmentReports:
        """
        Get all financial commitment reports - GET /financial_commitment_reports

        Returns:
            A FinancialCommitmentReports object which is a list of FinancialCommitmentReport objects
        """
        paginated_data = self._get_paginated("financial_commitment_reports")
        return FinancialCommitmentReports.model_validate(paginated_data)

    def get_financial_commitment_report(
        self, financial_commitment_report_token_params: FinancialCommitmentReportTokenParams
    ) -> FinancialCommitmentReport:
        """
        Retrieve a specific financial commitment report.

        GET /financial_commitment_reports/{financial_commitment_report_token}

        Args:
            financial_commitment_report_token_params: The token of the financial commitment report to retrieve

        Returns:
            The financial commitment report object
        """
        token_value = financial_commitment_report_token_params.financial_commitment_report_token
        data = self._get(f"financial_commitment_reports/{token_value}")
        return FinancialCommitmentReport.model_validate(data)

    def create_financial_commitment_report(
        self, new_financial_commitment_report: CreateFinancialCommitmentReport
    ) -> FinancialCommitmentReport:
        """
        Create a new financial commitment report - POST /financial_commitment_reports

        Args:
            new_financial_commitment_report: The new financial commitment report object to create

        Returns:
            The created financial commitment report object
        """
        data = self._post("financial_commitment_reports", new_financial_commitment_report)
        return FinancialCommitmentReport.model_validate(data)

    def update_financial_commitment_report(
        self,
        financial_commitment_report_token_params: FinancialCommitmentReportTokenParams,
        financial_commitment_report_update: UpdateFinancialCommitmentReport,
    ) -> FinancialCommitmentReport:
        """
        Update a specific financial commitment report.

        PUT /financial_commitment_reports/{financial_commitment_report_token}

        Args:
            financial_commitment_report_token_params: The token of the financial commitment report to update
            financial_commitment_report_update: The updated financial commitment report object

        Returns:
            The updated financial commitment report object
        """
        token_value = financial_commitment_report_token_params.financial_commitment_report_token
        data = self._put(f"financial_commitment_reports/{token_value}", financial_commitment_report_update)
        return FinancialCommitmentReport.model_validate(data)

    def delete_financial_commitment_report(
        self, financial_commitment_report_token_params: FinancialCommitmentReportTokenParams
    ) -> HttpStatusCode:
        """
        Delete a specific financial commitment report.

        DELETE /financial_commitment_reports/{financial_commitment_report_token}

        Args:
            financial_commitment_report_token_params: The token of the financial commitment report to delete

        Returns:
            The HTTP status code of the response
        """
        token_value = financial_commitment_report_token_params.financial_commitment_report_token
        return self._delete(f"financial_commitment_reports/{token_value}")

    # ---- Unit Costs APIs ----

    def get_all_unit_costs(self, query_params: UnitCostsGetParametersQuery) -> UnitCosts:
        """
        Get all unit costs - GET /unit_costs

        Args:
            query_params: Optional query parameters for filtering unit costs

        Returns:
            A UnitCosts object containing the unit costs data
        """
        paginated_data = self._get_paginated("unit_costs", query_params)
        return UnitCosts.model_validate(paginated_data)

    def create_unit_costs_data_export(self, unit_costs_export_request: UnitCostsDataExportsPostRequest) -> str:
        """
        Create a new unit costs data export - POST /unit_costs/data_exports

        Args:
            unit_costs_export_request: The request parameters for the unit costs data export

        Returns:
            str: The token of the created data export

        Note:
            This function returns the token of the created data export, which can be used to retrieve the export later.
            The export process is asynchronous, and the export may not be immediately available.
        """
        response = self.session.post(
            urljoin(self.base_url, "unit_costs/data_exports"),
            json=unit_costs_export_request.model_dump(exclude_none=True, by_alias=True),
            headers=self.session.headers,
            timeout=self._timeout,
        )
        response.raise_for_status()

        if response.is_success:
            location = response.headers.get("location")
            if location:
                # Split the entire location URL and get the last part
                token = location.split("/")[-1]
                return token
            else:
                raise ValueError("No location header found in response")
        else:
            error_details = response.json()
            error_message = f"Failed to create unit costs data export: {response.status_code}. Details: {error_details}"
            raise HTTPStatusError(error_message, request=response.request, response=response)

    # ---- User Feedback API ----

    def create_user_feedback(self, feedback: CreateUserFeedback) -> UserFeedback:
        """
        Create user feedback - POST /user_feedback

        Args:
            feedback: The feedback message to submit

        Returns:
            The created UserFeedback object
        """
        data = self._post("user_feedback", feedback)
        return UserFeedback.model_validate(data)

    # ---- Users APIs ----

    def get_all_users(self) -> Users:
        """
        Get all users - GET /users

        Returns:
            A Users object containing all users
        """
        paginated_data = self._get_paginated("users")
        return Users.model_validate(paginated_data)

    def get_user(self, user_token_params: UserTokenParams) -> User:
        """
        Get a specific user - GET /users/{user_token}

        Args:
            user_token_params: The token of the user to retrieve

        Returns:
            The User object
        """
        token = user_token_params.user_token
        data = self._get(f"users/{token}")
        return User.model_validate(data)

    # ---- Workspaces APIs ----

    def get_all_workspaces(self, query_params: WorkspacesGetParametersQuery | None = None) -> Workspaces:
        """
        Get all workspaces - GET /workspaces

        Args:
            query_params: Optional query parameters for filtering workspaces

        Returns:
            A Workspaces object containing all workspaces
        """
        paginated_data = self._get_paginated("workspaces", query_params)
        return Workspaces.model_validate(paginated_data)

    def get_workspace(self, workspace_token_params: WorkspaceTokenParams) -> Workspace:
        """
        Get a specific workspace - GET /workspaces/{workspace_token}

        Args:
            workspace_token_params: The token of the workspace to retrieve

        Returns:
            The Workspace object
        """
        token = workspace_token_params.workspace_token
        data = self._get(f"workspaces/{token}")
        return Workspace.model_validate(data)

    def create_workspace(self, workspace: CreateWorkspace) -> Workspace:
        """
        Create a new workspace - POST /workspaces

        Args:
            workspace: The workspace to create

        Returns:
            The created Workspace object
        """
        data = self._post("workspaces", workspace)
        return Workspace.model_validate(data)

    def update_workspace(
        self, workspace_token_params: WorkspaceTokenParams, workspace_update: WorkspacesWorkspaceTokenPutRequest
    ) -> Workspace:
        """
        Update a workspace - PUT /workspaces/{workspace_token}

        Args:
            workspace_token_params: The token of the workspace to update
            workspace_update: The updated workspace data

        Returns:
            The updated Workspace object
        """
        token = workspace_token_params.workspace_token
        data = self._put(f"workspaces/{token}", workspace_update)
        return Workspace.model_validate(data)

    def delete_workspace(self, workspace_token_params: WorkspaceTokenParams) -> HttpStatusCode:
        """
        Delete a workspace - DELETE /workspaces/{workspace_token}

        Args:
            workspace_token_params: The token of the workspace to delete

        Returns:
            The HTTP status code of the response
        """
        token = workspace_token_params.workspace_token
        return self._delete(f"workspaces/{token}")

    # ---- Audit Logs APIs ----

    def get_all_audit_logs(self, query_params: AuditLogsGetParametersQuery | None = None) -> AuditLogs:
        """
        Get all audit logs - GET /audit_logs

        Args:
            query_params: Optional query parameters for filtering audit logs.
                         Use object_token to filter by resource (e.g., cost report token)

        Returns:
            An AuditLogs object containing all audit logs (filtered if query_params provided)
        """
        paginated_data = self._get_paginated("audit_logs", query_params)
        return AuditLogs.model_validate(paginated_data)

    def get_audit_log(self, audit_log_token_params: AuditLogTokenParams) -> AuditLog:
        """
        Get a specific audit log - GET /audit_logs/{audit_log_token}

        Args:
            audit_log_token_params: The token of the audit log to retrieve

        Returns:
            The AuditLog object
        """
        token = audit_log_token_params.audit_log_token
        data = self._get(f"audit_logs/{token}")
        return AuditLog.model_validate(data)
