from ai_core_sdk.models.kpi import Kpi
from ai_core_sdk.resource_clients import BaseClient


class KpiClient(BaseClient):
    """KpiClient is a class implemented for interacting with the analytics kpi
    endpoint of the server. It implements the base class
    :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """
    __PATH = '/analytics/kpis'

    def query(self) -> Kpi:
        """Retrieves the number of executions, artifacts, and deployments
        for each resource group, scenario, and executable.

        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: The retrieved KPI data
        :rtype: class:`ai_core_sdk.models.kpi.Kpi`
        """
        response_dict = self.rest_client.get(path=f'{self.__PATH}')
        return Kpi.from_dict(response_dict)
