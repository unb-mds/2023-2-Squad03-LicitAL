from typing import Any, Dict, List

from .base_models import QueryResponse
from .execution import Execution


class ExecutionQueryResponse(QueryResponse):
    """The ExecutionQueryResponse object defines the response of the execution query request
    :param resources: List of the executions returned from the server
    :type resources: List[class:`ai_api_client_sdk.models.execution.Execution`]
    :param count: Total number of the queried executions
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, resources: List[Execution], count: int, **kwargs):
        super().__init__(resources=resources, count=count, **kwargs)

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.execution_query_response.ExecutionQueryResponse` object, created 
        from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.execution_query_response.ExecutionQueryResponse`
        """
        response_dict['resources'] = [Execution.from_dict(r) for r in response_dict['resources']]
        return ExecutionQueryResponse(**response_dict)
