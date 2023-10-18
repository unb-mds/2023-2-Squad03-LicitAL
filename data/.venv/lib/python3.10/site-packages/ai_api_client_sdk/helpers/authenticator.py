import requests

from ai_api_client_sdk.exception import AIAPIAuthenticatorException, AIAPIAuthenticatorInvalidRequestException, \
    AIAPIAuthenticatorAuthorizationException, AIAPIAuthenticatorServerException, \
    AIAPIAuthenticatorForbiddenException, AIAPIAuthenticatorMethodNotAllowedException, \
    AIAPIAuthenticatorTimeoutException


class Authenticator:
    """Authenticator class is implemented to retrieve the authorization token from the xsuaa server

    :param auth_url: URL of the authorization endpoint. Should be the full URL (including /oauth/token)
    :type auth_url: str
    :param client_id: client id to be used for authorization
    :type client_id: str
    :param client_secret: client secret to be used for authorization
    :type client_secret: str
    """

    def __init__(self, auth_url: str, client_id: str, client_secret: str):
        self.url: str = auth_url
        self.client_id: str = client_id
        self.client_secret: str = client_secret

    def get_token(self) -> str:
        """Retrieves the token from the xsuaa server.

        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthenticatorException` if an unexpected exception occurs while
            trying to retrieve the token
        :return: The Bearer token
        :rtype: str
        """
        data = {'grant_type': 'client_credentials', 'client_id': self.client_id, 'client_secret': self.client_secret}
        error_msg = None
        try:
            response = requests.post(url=self.url, data=data)
            status_code = response.status_code
            error_msg = response.text

        except Exception as exception:  # pylint:disable=broad-except
            raise AIAPIAuthenticatorException(status_code=500, error_message=error_msg) from exception

        if status_code == 400:
            raise AIAPIAuthenticatorInvalidRequestException(error_message=error_msg)
        elif status_code == 401:
            raise AIAPIAuthenticatorAuthorizationException(error_message=error_msg)
        elif status_code == 403:
            raise AIAPIAuthenticatorForbiddenException(error_message=error_msg)
        elif status_code == 405:
            raise AIAPIAuthenticatorMethodNotAllowedException(error_message=error_msg)
        elif status_code == 408:
            raise AIAPIAuthenticatorTimeoutException(error_message=error_msg)
        elif status_code // 100 != 2:
            raise AIAPIAuthenticatorServerException(status_code=status_code, error_message=error_msg)

        try:
            access_token = response.json()['access_token']
        except Exception as exception:  # pylint:disable=broad-except
            raise AIAPIAuthenticatorException(status_code=500, error_message=error_msg) from exception
        return f'Bearer {access_token}'
