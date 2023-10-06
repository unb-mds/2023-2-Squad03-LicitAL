from ai_core_sdk.helpers import form_top_skip_params
from ai_core_sdk.models import BasicResponse
from ai_core_sdk.models.base_models import Message
from ai_core_sdk.models.object_store_secret import ObjectStoreSecret
from ai_core_sdk.models.object_store_secret_query_response import ObjectStoreSecretQueryResponse
from ai_core_sdk.resource_clients import BaseClient


class ObjectStoreSecretsClient(BaseClient):
    """ObjectStoreSecretsClient is a class implemented for interacting with the object store secret related
    endpoints of the server. It implements the base class
    :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """
    __PATH = '/admin/objectStoreSecrets'

    def create(self, name: str, type: str, data: dict, bucket: str = None, endpoint: str = None, region: str = None,
               path_prefix: str = None, verifyssl: str = None, usehttps: str = None,
               resource_group: str = None) -> Message:
        """Creates an object store secret.

        :param name: name of the object store secret
        :type name: str
        :param type: type of object storage
        :type type: str
        :param data: data to be posted
        :type data: str
        :param bucket: name of the bucket
        :type bucket: str
        :param endpoint: endpoint of object storage
        :type endpoint: str
        :param region: region of object storage
        :type region: str
        :param path_prefix: path prefix
        :type path_prefix: str
        :param verifyssl: verify ssl
        :type verifyssl: str
        :param usehttps: use https
        :type usehttps: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_core_sdk.ai_core_v2_client.AICoreV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIForbiddenException` if a 403 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIConflictException` if a 409 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: A list of metadata of available secrets
        :rtype: class:`ai_core_sdk.models.base_models.BasicNameResponse`
        """
        body = {
            'name': name,
            'type': type,
            'data': data,
        }

        if bucket:
            body['bucket'] = bucket
        if endpoint:
            body['endpoint'] = endpoint
        if region:
            body['region'] = region
        if path_prefix:
            body['path_prefix'] = path_prefix
        if verifyssl:
            body['verifyssl'] = verifyssl
        if usehttps:
            body['usehttps'] = usehttps

        response_dict = self.rest_client.post(path=f'{self.__PATH}', body=body, resource_group=resource_group)
        return Message.from_dict(response_dict)

    def delete(self, name: str, resource_group: str = None) -> BasicResponse:
        """Deletes the object store secret.

        :param name: name of the object store secret to be deleted
        :type name: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_core_sdk.ai_core_v2_client.AICoreV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIForbiddenException` if a 403 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.base_models.BasicResponse`
        """
        response_dict = self.rest_client.delete(path=f'{self.__PATH}/{name}', resource_group=resource_group)
        return BasicResponse.from_dict(response_dict)

    def get(self, name: str, resource_group: str = None) -> ObjectStoreSecret:
        """Retrieves the object store secret from the server.

        :param name: name of the object store secret to be retrieved
        :type name: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_core_sdk.ai_core_v2_client.AICoreV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIForbiddenException` if a 403 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: The retrieved object store secret
        :rtype: class:`ai_core_sdk.models.object_store_secret.ObjectStoreSecret`
        """
        response_dict = self.rest_client.get(path=f'{self.__PATH}/{name}', resource_group=resource_group)
        return ObjectStoreSecret.from_dict(response_dict)

    def modify(self, name: str, type: str, data: dict, bucket: str = None, endpoint: str = None, region: str = None,
               path_prefix: str = None, verifyssl: str = None, usehttps: str = None,
               resource_group: str = None) -> BasicResponse:
        """Modifies the object store secret

        :param name: name of the object store secret to be modified
        :type name: str
        :param type: type of object storage
        :type type: str
        :param data: data to be posted
        :type data: str
        :param bucket: name of the bucket
        :type bucket: str
        :param endpoint: endpoint of object storage
        :type endpoint: str
        :param region: region of object storage
        :type region: str
        :param path_prefix: path prefix
        :type path_prefix: str
        :param verifyssl: verify ssl
        :type verifyssl: str
        :param usehttps: use https
        :type usehttps: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_core_sdk.ai_core_v2_client.AICoreV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIForbiddenException` if a 403 response is received from the
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
        body = {
            'name': name,
            'type': type,
            'data': data,
        }

        if bucket:
            body['bucket'] = bucket
        if endpoint:
            body['endpoint'] = endpoint
        if region:
            body['region'] = region
        if path_prefix:
            body['path_prefix'] = path_prefix
        if verifyssl:
            body['verifyssl'] = verifyssl
        if usehttps:
            body['usehttps'] = usehttps

        response_dict = self.rest_client.patch(path=f'{self.__PATH}/{name}', body=body, resource_group=resource_group)
        return BasicResponse.from_dict(response_dict)

    def query(self, top: int = None, skip: int = None, resource_group: str = None) -> ObjectStoreSecretQueryResponse:
        """Returns the object store secrets.

        :param top: Number of object store secrets to be retrieved, defaults to None
        :type top: int, optional
        :param skip: Number of object store secrets to be skipped, from the list of the queried object store
            secrets, defaults to None
        :type skip: int, optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_core_sdk.ai_core_v2_client.AICoreV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIForbiddenException` if a 403 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: A list of object store secrets
        :rtype: class:`ai_core_sdk.models.object_store_secret_query_response.ObjectStoreSecretQueryResponse`
        """
        params = form_top_skip_params(top, skip)
        response_dict = self.rest_client.get(path=f'{self.__PATH}', params=params, resource_group=resource_group)
        return ObjectStoreSecretQueryResponse.from_dict(response_dict)
