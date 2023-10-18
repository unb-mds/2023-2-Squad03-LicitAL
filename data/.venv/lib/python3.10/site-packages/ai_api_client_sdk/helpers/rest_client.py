import json
from typing import Callable, Dict, Union

import humps
import requests
from ai_api_client_sdk.helpers.constants import Timeouts
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from ai_api_client_sdk.exception import AIAPIAuthorizationException, AIAPIInvalidRequestException, \
    AIAPINotFoundException, AIAPIPreconditionFailedException, AIAPIRequestException, AIAPIServerException


class RestClient:
    """RestClient is the class implemented for sending the requests to the server.

    :param base_url: Base URL of the server. Should include the base path as well. (i.e., "<base_url>/scenarios" should
        work)
    :type base_url: str
    :param get_token: the function which returns the Bearer token, when called
    :type get_token: Callable[[], str]
    :param resource_group: The default resource group which will be used while sending the requests to the server,
        defaults to None
    :type resource_group: str
    :param client_type: Used for Metering to distinguish eg AI Launchpad python SDKs etc,
        defaults to None
    :type client_type: str
    :param read_timeout: Read timeout for requests in seconds, defaults to 60s
    :type read_timeout: int
    :param connect_timeout: Connect timeout for requests in seconds, defaults to 60s
    :type connect_timeout: int
    :param num_request_retries: Number of retries for failing requests with http status code 429, 500, 502, 503 or 504,
        defaults to 60s
    :type num_request_retries: int
    """

    def __init__(self, base_url: str, get_token: Callable[[], str], resource_group: str = None, client_type: str = None,
                 read_timeout=Timeouts.READ_TIMEOUT.value, connect_timeout=Timeouts.CONNECT_TIMEOUT.value,
                 num_request_retries=Timeouts.NUM_REQUEST_RETRIES.value):
        self.base_url: str = base_url
        self.get_token: Callable[[], str] = get_token
        self.resource_group_header: str = 'AI-Resource-Group'
        self.client_type_header: str = 'AI-Client-Type'
        self.headers: dict = {}
        if resource_group:
            self.headers[self.resource_group_header] = resource_group
        if client_type:
            self.headers[self.client_type_header] = client_type
        self.read_timeout = read_timeout
        self.connect_timeout = connect_timeout
        self.num_request_retries = num_request_retries

    def _handle_request(self, method: str, path: str, params: Dict[str, str] = None,
                        body_json: Dict[str, Union[str, dict]] = None, headers: Dict[str, str] = None,
                        resource_group: str = None) -> dict:
        error_description = f'Failed to {method.lower()} {path}'

        requests_session = requests.Session()

        retries = Retry(total=self.num_request_retries,
                        read=self.num_request_retries,
                        connect=self.num_request_retries,
                        status=self.num_request_retries,
                        backoff_factor=0.1,
                        status_forcelist=[429, 500, 502, 503, 504])

        requests_session.mount('http://', HTTPAdapter(max_retries=retries))
        requests_session.mount('https://', HTTPAdapter(max_retries=retries))

        requests_function = getattr(requests_session, method)
        url = f'{self.base_url}{path}'
        headers = headers or {}
        headers.update(self.headers.copy())
        headers['Authorization'] = self.get_token()
        if resource_group:
            headers[self.resource_group_header] = resource_group
        if body_json:
            body_json = humps.camelize(body_json)
        if params:
            params = humps.camelize(params)
        try:
            response = requests_function(url=url, params=params, json=body_json, headers=headers,
                                         timeout=(self.connect_timeout, self.read_timeout))
            if response.status_code == 401:
                raise AIAPIAuthorizationException(description=error_description, error_message=response.text)
            try:
                response_json = response.json()
            except json.decoder.JSONDecodeError:
                response_json = response.text
        except AIAPIAuthorizationException as ae:
            raise ae
        except Exception as e:
            raise AIAPIRequestException(error_description, 500) from e
        if type(response_json) is dict and 'error' in response_json:
            status_code = response.status_code
            error_message = response_json['error']['message']
            error_code = response_json['error']['code']
            request_id = response_json['error'].get('requestId')
            error_details = response_json['error'].get('details')
            if status_code == 400:
                raise AIAPIInvalidRequestException(description=error_description, error_message=error_message,
                                                   error_code=error_code, request_id=request_id, details=error_details)
            elif status_code == 404:
                raise AIAPINotFoundException(description=error_description, error_message=error_message,
                                             error_code=error_code, request_id=request_id, details=error_details)
            elif status_code == 412:
                raise AIAPIPreconditionFailedException(description=error_description, error_message=error_message,
                                                       error_code=error_code, request_id=request_id,
                                                       details=error_details)
            else:
                raise AIAPIServerException(status_code=status_code, description=error_description,
                                           error_message=error_message, error_code=error_code, request_id=request_id,
                                           details=error_details)
        elif response.status_code // 100 != 2:
            raise AIAPIServerException(description=error_description, error_message=response.text,
                                       status_code=response.status_code)
        return humps.decamelize(response_json)

    def post(self, path: str, body: Dict[str, Union[str, dict]] = None, headers: Dict[str, str] = None,
             resource_group: str = None) -> dict:
        """Sends a POST request to the server.

        :param path: path of the endpoint the request should be sent to
        :type path: str
        :param body: body of the request, defaults to None
        :type body: Dict[str, str], optional
        :param headers: headers of the request, defaults to None
        :type headers: Dict[str, str], optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this, or the
            resource_group property of this class should be set.
        :type resource_group: str
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
        :return: The JSON response from the server (The keys decamelized)
        :rtype: dict
        """
        return self._handle_request('post', path=path, body_json=body, headers=headers, resource_group=resource_group)

    def get(self, path: str, params: Dict[str, str] = None, headers: Dict[str, str] = None,
            resource_group: str = None) -> Union[dict, int]:
        """Sends a GET request to the server.

        :param path: path of the endpoint the request should be sent to
        :type path: str
        :param params: parameters of the request, defaults to None
        :type params: Dict[str, str], optional
        :param headers: headers of the request, defaults to None
        :type headers: Dict[str, str], optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this, or the
            resource_group property of this class should be set.
        :type resource_group: str
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
        :return: The JSON response from the server (The keys decamelized)
        :rtype: Union[dict, int]
        """
        return self._handle_request('get', path=path, params=params, headers=headers, resource_group=resource_group)

    def patch(self, path: str, body: Dict[str, Union[str, dict, list]], headers: Dict[str, str] = None,
              resource_group: str = None) -> dict:
        """Sends a PATCH request to the server.

        :param path: path of the endpoint the request should be sent to
        :type path: str
        :param body: body of the request
        :type body: Dict[str, Union[str, dict, list]]
        :param headers: headers of the request, defaults to None
        :type headers: Dict[str, str], optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this, or the
            resource_group property of this class should be set.
        :type resource_group: str
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
        :return: The JSON response from the server (The keys decamelized)
        :rtype: dict
        """
        return self._handle_request('patch', path=path, body_json=body, headers=headers, resource_group=resource_group)

    def delete(self, path: str, params: Dict[str, str] = None, headers: Dict[str, str] = None,
               resource_group: str = None) -> dict:
        """Sends a DELETE request to the server.

        :param path: path of the endpoint the request should be sent to
        :type path: str
        :param params: parameters of the request, defaults to None
        :type params: Dict[str, str], optional
        :param headers: headers of the request, defaults to None
        :type headers: Dict[str, str], optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this, or the
            resource_group property of this class should be set.
        :type resource_group: str
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
        :return: The JSON response from the server (The keys decamelized)
        :rtype: dict
        """
        return self._handle_request('delete', path=path, params=params, headers=headers, resource_group=resource_group)
