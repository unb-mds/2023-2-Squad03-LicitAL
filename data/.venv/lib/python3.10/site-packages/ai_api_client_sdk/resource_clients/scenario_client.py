from typing import List


from ai_api_client_sdk.models.scenario import Scenario
from ai_api_client_sdk.models.scenario_query_response import ScenarioQueryResponse
from ai_api_client_sdk.models.version_query_response import VersionQueryResponse
from ai_api_client_sdk.resource_clients.base_client import BaseClient


class ScenarioClient(BaseClient):
    """ScenarioClient is a class implemented for interacting with the scenario related endpoints of the server. It
    implements the base class :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """

    def get(self, scenario_id: str, resource_group: str = None) -> Scenario:
        """Retrieves the scenario from the server.

        :param scenario_id: ID of the scenario to be retrieved
        :type scenario_id: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: The retrieved scenario
        :rtype: class:`ai_api_client_sdk.models.scenario.Scenario`
        """
        scenario_dict = self.rest_client.get(path=f'/scenarios/{scenario_id}', resource_group=resource_group)
        return Scenario.from_dict(scenario_dict)

    def query(self, resource_group: str = None) -> ScenarioQueryResponse:
        """Queries the scenarios.

        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.scenario_query_response.ScenarioQueryResponse`
        """
        response_dict = self.rest_client.get(path='/scenarios', resource_group=resource_group)
        return ScenarioQueryResponse.from_dict(response_dict)

    def query_versions(self, scenario_id: str, label_selector: List[str] = None, resource_group: str = None) -> \
            VersionQueryResponse:
        """Queries the versions.

        :param scenario_id: ID of the scenario, the versions should belong to
        :type scenario_id: str
        :param label_selector: list of the label selector strings in the form of "key=value" or "key!=value", to filter
            the scenarios with respect to their labels, defaults to None
        :type label_selector: List[str], optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.scenario_query_response.ScenarioQueryResponse`
        """
        params = self._form_query_params(label_selector=label_selector)
        response_dict = self.rest_client.get(path=f'/scenarios/{scenario_id}/versions', params=params,
                                             resource_group=resource_group)
        return VersionQueryResponse.from_dict(response_dict)
