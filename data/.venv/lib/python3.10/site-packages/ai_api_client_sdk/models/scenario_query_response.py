from typing import Any, Dict, List

from .base_models import QueryResponse
from .scenario import Scenario


class ScenarioQueryResponse(QueryResponse):
    """The ScenarioQueryResponse object defines the response of the scenario query request
    :param resources: List of the scenarios returned from the server
    :type resources: List[class:`ai_api_client_sdk.models.scenario.Scenario`]
    :param count: Total number of the queried scenarios
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, resources: List[Scenario], count: int, **kwargs):
        super().__init__(resources=resources, count=count, **kwargs)

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.scenario_query_response.ScenarioQueryResponse` object, created
        from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.scenario_query_response.ScenarioQueryResponse`
        """
        response_dict['resources'] = [Scenario.from_dict(r) for r in response_dict['resources']]
        return ScenarioQueryResponse(**response_dict)
