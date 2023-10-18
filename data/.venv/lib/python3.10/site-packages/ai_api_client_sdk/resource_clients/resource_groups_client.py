from typing import List

from ai_api_client_sdk.models.base_models import BasicResponse
from ai_api_client_sdk.models.label import Label
from ai_api_client_sdk.models.resource_group import ResourceGroup
from ai_api_client_sdk.models.resource_group_query_response import ResourceGroupQueryResponse
from ai_api_client_sdk.resource_clients.base_client import BaseClient


class ResourceGroupsClient(BaseClient):
    """ResourceGroupsClient is a class implemented for interacting with the resource groups endpoints of the server.
    It implements the base class
    :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """
    __PATH = '/admin/resourceGroups'

    def create(self, resource_group_id: str, labels: List[Label] = None) -> ResourceGroup:
        """Creates resource group for a given tenant.

        :param resource_group_id: the id of the resource group and the length must be between 3 and 10 characters.
        :type resource_group_id: str
        :param labels: key-value pairs of the labels that will be added to the resource group.
        :type labels: List[Label]
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_core_sdk.models.resource_group.ResourceGroup`
        """
        body = {
            'resourceGroupId': resource_group_id,
        }

        if labels:
            body['labels'] = [l.to_dict() for l in labels]

        response_dict = self.rest_client.post(path=f'{self.__PATH}', body=body)
        return ResourceGroup.from_dict(response_dict)

    def delete(self, resource_group_id: str) -> BasicResponse:
        """Deletes the resource group.

        :param resource_group_id: the id of the resource group to be deleted
        :type resource_group_id: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIPreconditionFailedException` if a 412 response is received from
            the server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.base_models.BasicResponse`
        """
        response_dict = self.rest_client.delete(path=f'{self.__PATH}/{resource_group_id}')
        return BasicResponse.from_dict(response_dict)

    def get(self, resource_group_id: str) -> ResourceGroup:
        """Gets a resource group of a given tenant.

        :param resource_group_id: the id of the resource group to be retrieved
        :type resource_group_id: str
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
        :return: An object representing the resource group from the server
        :rtype: class:`ai_core_sdk.models.resource_group.ResourceGroup`
        """
        response_dict = self.rest_client.get(path=f'{self.__PATH}/{resource_group_id}')
        return ResourceGroup.from_dict(response_dict)

    def modify(self, resource_group_id: str, labels: List[Label]) -> None:
        """Modifies a resource group.

        :param resource_group_id: the id of the resource group
        :type resource_group_id: str
        :param labels: key-value pairs of the labels that will be added to the resource group.
        :type labels: List[Label]
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIPreconditionFailedException` if a 412 response is received from
            the server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        """

        body = {
            'resourceGroupId': resource_group_id,
            'labels': [l.to_dict() for l in labels],
        }

        self.rest_client.patch(path=f'{self.__PATH}/{resource_group_id}', body=body)

    def query(self, search: str = None, search_case_insensitive: bool = None) -> ResourceGroupQueryResponse:
        """Get all resource groups.

        :param search: Generic search term to be looked for in various attributes of resource groups, defaults to None
        :type search: str, optional
        :param search_case_insensitive: Indicates whether the search should be case insensitive
        :type search_case_insensitive: bool, optional
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: A list of resource groups for a given tenant.
        :rtype: class:`ai_core_sdk.models.resource_group_query_response.ResourceGroupQueryResponse`
        """
        params = self._form_query_params(search=search, search_case_insensitive=search_case_insensitive)
        response_dict = self.rest_client.get(path=f'{self.__PATH}', params=params)
        return ResourceGroupQueryResponse.from_dict(response_dict)
