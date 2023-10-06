class AIAPIClientSDKException(Exception):
    """Base Exception class for AI API Client SDK exceptions"""

    def __init__(self, description: str, status_code: int = None, error_message: str = None):
        msg = f'{description}: {error_message}' if error_message else description
        super().__init__(msg)
        self.description = description
        self.status_code = status_code
        self.error_message = error_message


class AIAPIInvalidInputException(AIAPIClientSDKException):
    """Exception type raised, when the provided input is invalid"""
    def __init__(self, description: str):
        super().__init__(description=description)


class AIAPIAuthenticatorException(AIAPIClientSDKException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.authenticator.Authenticator`"""

    def __init__(self, status_code: int = None, error_message: str = None):
        super().__init__(description='Could not retrieve Authorization token', status_code=status_code,
                         error_message=error_message)


class AIAPIAuthenticatorInvalidRequestException(AIAPIAuthenticatorException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.authenticator.Authenticator` if
    the XSUAA server responded with bad request when trying to retrieve a token"""

    def __init__(self, error_message: str = None):
        super().__init__(status_code=400, error_message=error_message)


class AIAPIAuthenticatorAuthorizationException(AIAPIAuthenticatorException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.authenticator.Authenticator` if
    the XSUAA server responded with unauthorized when trying to retrieve a token"""

    def __init__(self, error_message: str = None):
        super().__init__(status_code=401, error_message=error_message)


class AIAPIAuthenticatorForbiddenException(AIAPIAuthenticatorException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.authenticator.Authenticator` if
    the XSUAA server responded with forbidden when trying to retrieve a token"""

    def __init__(self, error_message: str = None):
        super().__init__(status_code=403, error_message=error_message)


class AIAPIAuthenticatorMethodNotAllowedException(AIAPIAuthenticatorException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.authenticator.Authenticator` if
    the XSUAA server responded with method not allowed when trying to retrieve a token"""

    def __init__(self, error_message: str = None):
        super().__init__(status_code=405, error_message=error_message)


class AIAPIAuthenticatorTimeoutException(AIAPIAuthenticatorException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.authenticator.Authenticator` if
    the XSUAA server responded with request timeout when trying to retrieve a token"""

    def __init__(self, error_message: str = None):
        super().__init__(status_code=408, error_message=error_message)


class AIAPIAuthenticatorServerException(AIAPIAuthenticatorException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.authenticator.Authenticator` if
    the XSUAA server responded with server error when trying to retrieve a token"""

    def __init__(self, status_code: int = None, error_message: str = None):
        super().__init__(status_code=status_code, error_message=error_message)


class AIAPIRequestException(AIAPIClientSDKException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.rest_client.RestClient` if an unexpected
    exception occurs while trying to send a request to the server
    """

    def __init__(self, description: str, status_code: int = None, error_message: str = None):
        super().__init__(description=description, status_code=status_code, error_message=error_message)


class AIAPIServerException(Exception):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.rest_client.RestClient`, if a non-2XX
    response is received from the server.

    :param description: description of the exception
    :type description: str
    :param status_code: Status code of the response from the server
    :type status_code: int
    :param error_message: Error message received from the server
    :type error_message: str
    :param error_code: Error code received from the server, defaults to None
    :type error_code: str, optional
    :param request_id: ID of the request, the response belongs to, defaults to None
    :type request_id: str, optional
    :param details: Error details received from the server, defaults to None
    :type details: dict, optional
    """

    def __init__(self, description: str, status_code: int, error_message: str, error_code: str = None,
                 request_id: str = None, details: dict = None):
        super().__init__()
        self.description = description
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
        self.request_id = request_id
        self.details = details

    def __str__(self):
        debug_msg = f'{self.description}: {self.error_message} \n ' \
                    f'Status Code: {self.status_code}, Request ID:{self.request_id}'
        return debug_msg


class AIAPIAuthorizationException(AIAPIServerException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.rest_client.RestClient` if a 401 response
    is received from the server. This extends the :class:`ai_api_client_sdk.exception.AIAPIServerException`, refer there
    for object definition
    """

    def __init__(self, description: str, error_message: str, error_code: str = None, request_id: str = None,
                 details: dict = None):
        super().__init__(description=description, status_code=401, error_code=error_code, error_message=error_message,
                         request_id=request_id, details=details)


class AIAPIInvalidRequestException(AIAPIServerException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.rest_client.RestClient` if a 400 response
    is received from the server. This extends the :class:`ai_api_client_sdk.exception.AIAPIServerException`, refer there
    for object definition
    """

    def __init__(self, description: str, error_code: str, error_message: str, request_id: str, details: dict = None):
        super().__init__(description=description, status_code=400, error_code=error_code, error_message=error_message,
                         request_id=request_id, details=details)


class AIAPINotFoundException(AIAPIServerException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.rest_client.RestClient` if a 404 response
    is received from the server. This extends the :class:`ai_api_client_sdk.exception.AIAPIServerException`, refer there
    for object definition
    """

    def __init__(self, description: str, error_code: str, error_message: str, request_id: str, details: dict = None):
        super().__init__(description=description, status_code=404, error_code=error_code, error_message=error_message,
                         request_id=request_id, details=details)


class AIAPIPreconditionFailedException(AIAPIServerException):
    """Exception type that is raised by the :class:`ai_api_client_sdk.helpers.rest_client.RestClient` if a 412 response
    is received from the server. This extends the :class:`ai_api_client_sdk.exception.AIAPIServerException`, refer there
    for object definition
    """

    def __init__(self, description: str, error_code: str, error_message: str, request_id: str, details: dict = None):
        super().__init__(description=description, status_code=412, error_code=error_code, error_message=error_message,
                         request_id=request_id, details=details)
