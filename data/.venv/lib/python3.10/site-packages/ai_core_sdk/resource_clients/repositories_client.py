from ai_core_sdk.models import BasicResponse
from ai_core_sdk.models.base_models import Message
from ai_core_sdk.models.repository import Repository
from ai_core_sdk.models.repository_query_response import RepositoryQueryResponse
from ai_core_sdk.resource_clients import BaseClient


class RepositoriesClient(BaseClient):
    """RepositoriesClient is a class implemented for interacting with the repositories related
    endpoints of the server. It implements the base class
    :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """
    __PATH = '/admin/repositories'

    def create(self, name: str, url: str, username: str, password: str) -> Message:
        """On-boards a new GitOps repository

        :param name: name of the GitOps repository
        :type name: str
        :param url: url of the GitOps repository
        :type url: str
        :param username: username to the GitOps repository
        :type username: str
        :param password: password to the GitOps repository
        :type password: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_core_sdk.models.base_models.BasicNameResponse`
        """
        body = {'name': name, 'url': url, 'username': username, 'password': password}
        response_dict = self.rest_client.post(path=self.__PATH, body=body)
        return Message.from_dict(response_dict)

    def delete(self, name: str) -> BasicResponse:
        """Off-boards a GitOps repository.

        :param name: name of the repository to be deleted
        :type name: str
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
        response_dict = self.rest_client.delete(path=f'{self.__PATH}/{name}')
        return BasicResponse.from_dict(response_dict)

    def get(self, name: str) -> Repository:
        """Retrieves the access details for a repository if it exists.

        :param name: name of the repository to be retrieved
        :type name: str
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
        :return: The access details for a repository
        :rtype: class:`ai_core_client_sdk.models.docker_registry_secret.DockerRegistrySecret`
        """
        response_dict = self.rest_client.get(path=f'{self.__PATH}/{name}')
        return Repository.from_dict(response_dict)

    def modify(self, name: str, username: str, password: str) -> BasicResponse:
        """Updates the referenced repository credentials to synchronize repository.

        :param name: name of the repository to be modified
        :type name: str
        :param username: username to the repository
        :type username: str
        :param password: password to the repository
        :type password: str
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
        :rtype: class:`ai_api_client_sdk.models.base_models.BasicResponse`
        """
        body = {'username': username, 'password': password}
        response_dict = self.rest_client.patch(path=f'{self.__PATH}/{name}', body=body)
        return BasicResponse.from_dict(response_dict)

    def query(self) -> RepositoryQueryResponse:
        """Retrieves a list of all GitOps repositories for a tenant.

        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: A list all GitOps repositories for a tenant
        :rtype: class:`ai_core_client_sdk.models.repository_query_response.RepositoryQueryResponse`
        """
        response_dict = self.rest_client.get(path=self.__PATH)
        return RepositoryQueryResponse.from_dict(response_dict)
