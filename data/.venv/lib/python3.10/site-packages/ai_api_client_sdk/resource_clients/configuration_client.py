from typing import List

from ai_api_client_sdk.models.configuration import Configuration
from ai_api_client_sdk.models.configuration_create_response import ConfigurationCreateResponse
from ai_api_client_sdk.models.configuration_query_response import ConfigurationQueryResponse
from ai_api_client_sdk.models.input_artifact_binding import InputArtifactBinding
from ai_api_client_sdk.models.parameter_binding import ParameterBinding
from ai_api_client_sdk.resource_clients.base_client import BaseClient


class ConfigurationClient(BaseClient):
    """ConfigurationClient is a class implemented for interacting with the configuration related endpoints of the
    server. It implements the base class :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """

    def create(self, name: str, scenario_id: str, executable_id: str, parameter_bindings: List[ParameterBinding] = None,
               input_artifact_bindings: List[InputArtifactBinding] = None,
               resource_group: str = None) -> ConfigurationCreateResponse:
        """Creates a configuration.

        :param name: Name of the configuration
        :type name: str
        :param scenario_id: ID of the scenario which the configuration should belong to
        :type scenario_id: str
        :param executable_id: ID of the executable, which should be configured
        :type executable_id: str
        :param parameter_bindings: List of the input parameters, defaults to None
        :type parameter_bindings: List[class:`ai_api_client_sdk.models.parameter_binding.ParameterBinding`], optional
        :param input_artifact_bindings: List of the input artifacts which are to be used by the executable,
            defaults to None
        :type input_artifact_bindings:
            List[class:`ai_api_client_sdk.models.input_artifact_binding.InputArtifactBinding`], optional
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
        :rtype: class:`ai_api_client_sdk.models.configuration_create_response.ConfigurationCreateResponse`
        """
        body = {
            'name': name,
            'scenario_id': scenario_id,
            'executable_id': executable_id
        }
        if parameter_bindings:
            body['parameter_bindings'] = [pb.to_dict() for pb in parameter_bindings]
        if input_artifact_bindings:
            body['input_artifact_bindings'] = [iab.to_dict() for iab in input_artifact_bindings]
        response_dict = self.rest_client.post(path='/configurations', body=body, resource_group=resource_group)
        return ConfigurationCreateResponse.from_dict(response_dict)

    def get(self, configuration_id: str, expand: str = None, resource_group: str = None) -> Configuration:
        """Retrieves the configuration from the server.

        :param configuration_id: ID of the configuration to be retrieved
        :type configuration_id: str
        :param expand: Entity whose details to be displayed in the response, defaults to None
        :type expand: str, optional
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
        :return: The retrieved configuration
        :rtype: class:`ai_api_client_sdk.models.configuration.Configuration`
        """
        params = self._form_query_params(expand=expand)
        configuration_dict = self.rest_client.get(path=f'/configurations/{configuration_id}', params=params,
                                                  resource_group=resource_group)
        return Configuration.from_dict(configuration_dict)

    def query(self, scenario_id: str = None, executable_ids: List[str] = None, top: int = None, skip: int = None,
              search: str = None, search_case_insensitive: bool = None, expand: str = None,
              resource_group: str = None) -> ConfigurationQueryResponse:
        """Queries the configurations.

        :param scenario_id: ID of the scenario the configurations should belong to, defaults to None
        :type scenario_id: str, optional
        :param executable_ids: IDs of the executables the configurations should have configured, defaults to None
        :type executable_ids: List[str], optional
        :param top: Number of configurations to be retrieved, defaults to None
        :type top: int, optional
        :param skip: Number of configurations to be skipped, from the list of the queried configurations, defaults to
            None
        :type skip: int, optional
        :param search: Generic search term to be looked for in various attributes of configurations, defaults to None
        :type search: str, optional
        :param search_case_insensitive: Indicates whether the search should be case insensitive
        :type search_case_insensitive: bool, optional
        :param expand: Entity whose details to be displayed in the response, defaults to None
        :type expand: str, optional
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
        :rtype: class:`ai_api_client_sdk.models.configuration_query_response.ConfigurationQueryResponse`
        """
        params = self._form_query_params(scenario_id=scenario_id, executable_ids=executable_ids, top=top, skip=skip,
                                         search=search, search_case_insensitive=search_case_insensitive, expand=expand)
        response_dict = self.rest_client.get(path='/configurations', params=params, resource_group=resource_group)
        return ConfigurationQueryResponse.from_dict(response_dict)

    def count(self, scenario_id: str = None, executable_ids: List[str] = None, search: str = None,
              resource_group: str = None) -> int:
        """Counts the configurations.

        :param scenario_id: ID of the scenario the configurations should belong to, defaults to None
        :type scenario_id: str, optional
        :param executable_ids: IDs of the executables the configurations should have configured, defaults to None
        :type executable_ids: List[str], optional
        :param search: Generic search term to be looked for in various attributes of configurations, defaults to None
        :type search: str, optional
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
        :rtype: int
        """
        params = self._form_query_params(scenario_id=scenario_id, executable_ids=executable_ids, search=search)
        return self.rest_client.get(path='/configurations/$count', params=params, resource_group=resource_group)
