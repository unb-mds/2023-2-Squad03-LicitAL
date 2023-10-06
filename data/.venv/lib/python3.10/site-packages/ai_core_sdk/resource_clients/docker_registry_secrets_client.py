from ai_core_sdk.helpers import form_top_skip_params
from ai_core_sdk.models import BasicResponse
from ai_core_sdk.models.base_models import Message
from ai_core_sdk.models.docker_registry_secret import DockerRegistrySecret
from ai_core_sdk.models.docker_registry_secret_query_response import DockerRegistrySecretQueryResponse
from ai_core_sdk.resource_clients import BaseClient


class DockerRegistrySecretsClient(BaseClient):
    """DockerRegistrySecretsClient is a class implemented for interacting with the docker registry secret related
    endpoints of the server. It implements the base class
    :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """
    __PATH = '/admin/dockerRegistrySecrets'

    def create(self, name: str, data: dict) -> Message:
        """Creates a docker secret based on the configuration in the request body.

        :param name: name of the docker registry secret
        :type name: str
        :param data: json dict, defining the docker registry secret
        :type data: dict
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_core_sdk.models.base_models.Message`
        """
        body = {'name': name, 'data': data}
        response_dict = self.rest_client.post(path=f'{self.__PATH}', body=body)
        return Message.from_dict(response_dict)

    def delete(self, name: str) -> BasicResponse:
        """Deletes the docker registry secret with the given name if it exists.

        :param name: name of the docker registry secret to be deleted
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

    def get(self, name: str) -> DockerRegistrySecret:
        """Returns the metadata of the docker registry secrets which matches the given name.

        :param name: name of the docker registry secret to be retrieved
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
        :return: The retrieved metadata of the docker registry secret
        :rtype: class:`ai_core_sdk.models.docker_registry_secret.DockerRegistrySecret`
        """
        response_dict = self.rest_client.get(path=f'{self.__PATH}/{name}')
        return DockerRegistrySecret.from_dict(response_dict)

    def modify(self, name: str, data: dict) -> BasicResponse:
        """Updates the docker registry secret

        :param name: name of the docker registry secret to be modified
        :type name: str
        :param data: json dict, defining the docker registry secret
        :type data: dict
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
        body = {'data': data}
        response_dict = self.rest_client.patch(path=f'{self.__PATH}/{name}', body=body)
        return BasicResponse.from_dict(response_dict)

    def query(self, top: int = None, skip: int = None) -> DockerRegistrySecretQueryResponse:
        """Gets a list of metadata of docker registry secrets.

        :param top: Number of docker registry secrets to be retrieved, defaults to None
        :type top: int, optional
        :param skip: Number of docker registry secrets to be skipped, from the list of the queried docker registry
            secrets, defaults to None
        :type skip: int, optional
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: A list of metadata of secrets
        :rtype: class:`ai_core_sdk.models.docker_registry_secret_query_response.DockerRegistrySecretQueryResponse`
        """
        params = form_top_skip_params(top, skip)
        response_dict = self.rest_client.get(path=f'{self.__PATH}', params=params)
        return DockerRegistrySecretQueryResponse.from_dict(response_dict)
