from ai_core_sdk.exception import AICoreInvalidInputException
from ai_core_sdk.models import BasicResponse
from ai_core_sdk.models.application import Application
from ai_core_sdk.models.application_query_response import ApplicationQueryResponse
from ai_core_sdk.models.application_status import ApplicationStatus
from ai_core_sdk.resource_clients import BaseClient


class ApplicationsClient(BaseClient):
    """ApplicationsClient is a class implemented for interacting with the applications related
    endpoints of the server. It implements the base class
    :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """

    __PATH = '/admin/applications'

    def create(self, revision: str, path: str, application_name: str = None, repository_name: str = None,
               repository_url: str = None) -> BasicResponse:
        """Creates an application.

        :param revision: revision to synchronize
        :type revision: str
        :param path: within the repository to synchronize
        :type path: str
        :param application_name: Name of the application
        :type application_name: str, optional
        :param repository_name: Name of the repository to synchronize. Either this or the repository_url needs to be
            provided
        :type repository_name: str, optional
        :param repository_url: URL of the repository to synchronize. Either this or the repository_name needs to be
            provided
        :type repository_url: str, optional
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.base_models.BasicResponse`
        """
        if (repository_url and repository_name) or (not repository_name and not repository_url):
            raise AICoreInvalidInputException('Either repository_url or repository_name must be provided, not both')
        body = {'revision': revision, 'path': path}
        if repository_name:
            body['repository_name'] = repository_name
        elif repository_url:
            body['repository_url'] = repository_url
        if application_name:
            body['application_name'] = application_name
        response_dict = self.rest_client.post(path=self.__PATH, body=body)
        return BasicResponse.from_dict(response_dict)

    def delete(self, application_name: str) -> BasicResponse:
        """Deletes the application.

        :param application_name: name of the application to be deleted
        :type application_name: str
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
        response_dict = self.rest_client.delete(path=f'{self.__PATH}/{application_name}')
        return BasicResponse.from_dict(response_dict)

    def get(self, application_name: str) -> Application:
        """Retrieves the application from the server.

        :param application_name: name of the application to be retrieved
        :type application_name: str
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
        :return: The retrieved application
        :rtype: class:`ai_core_sdk.models.application.Application`
        """
        response_dict = self.rest_client.get(path=f'{self.__PATH}/{application_name}')
        return Application.from_dict(response_dict)

    def get_status(self, application_name: str) -> ApplicationStatus:
        """Retrieves the application status from the server.

        :param application_name: name of the application
        :type application_name: str
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
        :return: The retrieved application status
        :rtype: class:`ai_core_sdk.models.application_status.ApplicationStatus`
        """
        response_dict = self.rest_client.get(path=f'{self.__PATH}/{application_name}/status')
        return ApplicationStatus.from_dict(response_dict)

    def modify(self, application_name: str, repository_url: str, path: str, revision: str) -> BasicResponse:
        """Modifies the application

        :param application_name: name of the application to be modified
        :type name: str
        :param repository_url:
        :type repository_url: str
        :param revision:
        :type revision: str
        :param path:
        :type path: str
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
        body = {'path': path, 'revision': revision, 'repository_url': repository_url}
        response_dict = self.rest_client.patch(path=f'{self.__PATH}/{application_name}', body=body)
        return BasicResponse.from_dict(response_dict)

    def query(self) -> ApplicationQueryResponse:
        """Returns the applications.

        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: The retrieved applications
        :rtype: class:`ai_core_sdk.models.application_query_response.ApplicationQueryResponse`
        """
        response_dict = self.rest_client.get(path=self.__PATH)
        return ApplicationQueryResponse.from_dict(response_dict)

    def refresh(self, application_name: str) -> BasicResponse:
        """Triggers synchronisation of the application.

        :param application_name: name of the application to be refreshed
        :type application_name: str
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
        response_dict = self.rest_client.post(path=f'{self.__PATH}/{application_name}/refresh')
        return BasicResponse.from_dict(response_dict)
