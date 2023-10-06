from ai_api_client_sdk.exception import AIAPIAuthenticatorException, AIAPIAuthorizationException, \
    AIAPIInvalidRequestException, AIAPINotFoundException, AIAPIPreconditionFailedException, AIAPIRequestException, \
    AIAPIServerException


class AICoreSDKException(Exception):
    """Base Exception class for AI Core SDK exceptions"""


class AICoreInvalidInputException(AICoreSDKException):
    """Exception thrown in case of invalid input"""
