from typing import Any, Dict

from .base_models import BasicResponse


class ConfigurationCreateResponse(BasicResponse):
    """The ConfigurationCreateResponse object defines the response of the configuration create request. Refer to
    :class:`ai_api_client_sdk.models.base_models.BasicResponse`, for the object definition
    """
    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.configuration_create_response.ConfigurationCreateResponse` object,
        created from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.configuration_create_response.ConfigurationCreateResponse`
        """
        return ConfigurationCreateResponse(**response_dict)
