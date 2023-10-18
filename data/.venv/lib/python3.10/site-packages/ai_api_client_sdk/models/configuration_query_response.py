from typing import Any, Dict, List

from .base_models import QueryResponse
from .configuration import Configuration


class ConfigurationQueryResponse(QueryResponse):
    """The ConfigurationQueryResponse object defines the response of the configuration query request
    :param resources: List of the configurations returned from the server
    :type resources: List[class:`ai_api_client_sdk.models.configuration.Configuration`]
    :param count: Total number of the queried configurations
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, resources: List[Configuration], count: int, **kwargs):
        super().__init__(resources=resources, count=count, **kwargs)

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.configuration_query_response.ConfigurationQueryResponse` object,
        created from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.configuration_query_response.ConfigurationQueryResponse`
        """
        response_dict['resources'] = [Configuration.from_dict(r) for r in response_dict['resources']]
        return ConfigurationQueryResponse(**response_dict)
