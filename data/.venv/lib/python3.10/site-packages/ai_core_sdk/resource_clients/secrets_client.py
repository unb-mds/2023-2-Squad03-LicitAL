from ai_core_sdk.helpers import form_top_skip_params
from ai_core_sdk.models import BasicResponse
from ai_core_sdk.models.base_models import Message
from ai_core_sdk.models.secret_query_response import SecretQueryResponse
from ai_core_sdk.resource_clients import BaseClient


class SecretsClient(BaseClient):
    """SecretsClient is a class implemented for interacting with the secret related
    endpoints of the server. It implements the base class
    :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """
    __PATH = '/admin/secrets'

    def create(self, name: str, data: dict, resource_group: str = None, ai_tenant_scope=True) -> Message:
        """Creates a secret.

        :param name: name of the secret
        :type name: str
        :param data: data of secret
        :type data: dict
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_core_sdk.ai_core_v2_client.AICoreV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :param ai_tenant_scope: Specify whether the main tenant scope is to be used
        :type ai_tenant_scope: bool
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
        :rtype: class:`ai_core_sdk.models.base_models.Message`
        """
        body = {
            'name': name,
            'data': data,
        }
        headers = {'AI-Tenant-Scope': str(ai_tenant_scope).lower()}

        response_dict = self.rest_client.post(path=f'{self.__PATH}', body=body, resource_group=resource_group,
                                              headers=headers)
        return Message.from_dict(response_dict)

    def delete(self, name: str, resource_group: str = None, ai_tenant_scope=True) -> Message:
        """Deletes the secret.

        :param name: name of the secret to be deleted
        :type name: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_core_sdk.ai_core_v2_client.AICoreV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :param ai_tenant_scope: Specify whether the main tenant scope is to be used
        :type ai_tenant_scope: bool
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
        :rtype: class:`ai_api_client_sdk.models.base_models.Message`
        """
        headers = {'AI-Tenant-Scope': str(ai_tenant_scope).lower()}

        response_dict = self.rest_client.delete(path=f'{self.__PATH}/{name}', resource_group=resource_group,
                                                headers=headers)
        if response_dict == 200:
            response_dict = { "message": "Secret has been deleted" }
        return Message.from_dict(response_dict)

    def modify(self, name: str, data: dict, resource_group: str = None, ai_tenant_scope=True) -> Message:
        """Modifies the secret.

        :param name: name of the secret to be modified
        :type name: str
        :param data: data of secret
        :type data: dict
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_core_sdk.ai_core_v2_client.AICoreV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :param ai_tenant_scope: Specify whether the main tenant scope is to be used
        :type ai_tenant_scope: bool
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
        :rtype: class:`ai_api_client_sdk.models.base_models.Message`
        """
        body = {
            'data': data,
        }
        headers = {'AI-Tenant-Scope': str(ai_tenant_scope).lower()}

        response_dict = self.rest_client.patch(path=f'{self.__PATH}/{name}', body=body, resource_group=resource_group,
                                               headers=headers)
        return Message.from_dict(response_dict)

    def query(self, top: int = None, skip: int = None, resource_group: str = None,
              ai_tenant_scope: bool = True) -> SecretQueryResponse:
        """Returns the secrets.

        :param top: Number of secrets to be retrieved, defaults to None
        :type top: int, optional
        :param skip: Number of secrets to be skipped, from the list of the queried secrets, defaults to None
        :type skip: int, optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_core_sdk.ai_core_v2_client.AICoreV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :param ai_tenant_scope: Specify whether the main tenant scope is to be used
        :type ai_tenant_scope: bool
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
        :return: A list of secrets
        :rtype: class:`ai_core_sdk.models.secret_query_response.SecretQueryResponse`
        """
        params = form_top_skip_params(top, skip)
        headers = {'AI-Tenant-Scope': str(ai_tenant_scope).lower()}

        response_dict = self.rest_client.get(path=f'{self.__PATH}', params=params, headers=headers,
                                             resource_group=resource_group)
        return SecretQueryResponse.from_dict(response_dict)
