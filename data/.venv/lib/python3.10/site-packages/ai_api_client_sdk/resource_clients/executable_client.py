from ai_api_client_sdk.models.executable import Executable
from ai_api_client_sdk.models.executable_query_response import ExecutableQueryResponse
from ai_api_client_sdk.resource_clients.base_client import BaseClient


class ExecutableClient(BaseClient):
    """ExecutableClient is a class implemented for interacting with the executable related endpoints of the server. It
    implements the base class :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """

    def get(self, scenario_id: str, executable_id: str, resource_group: str = None) -> Executable:
        """Retrieves the executable from the server.

        :param scenario_id: ID of the scenario the executable belongs to
        :type scenario_id: str
        :param executable_id: ID of the executable to be retrieved
        :type executable_id: str
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
        :return: The retrieved executable
        :rtype: class:`ai_api_client_sdk.models.executable.Executable`
        """
        executable_dict = self.rest_client.get(path=f'/scenarios/{scenario_id}/executables/{executable_id}',
                                               resource_group=resource_group)
        return Executable.from_dict(executable_dict)

    def query(self, scenario_id: str, version_id: str = None, resource_group: str = None) -> ExecutableQueryResponse:
        """Queries the executables.

        :param scenario_id: ID of the scenario the executables should belong to, defaults to None
        :type scenario_id: str, optional
        :param version_id: ID of the version, the executions should have, defaults to None
        :type version_id: str, optional
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
        :rtype: class:`ai_api_client_sdk.models.executable_query_response.ExecutableQueryResponse`
        """
        params = self._form_query_params(version_id=version_id)
        response_dict = self.rest_client.get(path=f'/scenarios/{scenario_id}/executables', params=params,
                                             resource_group=resource_group)
        return ExecutableQueryResponse.from_dict(response_dict)
