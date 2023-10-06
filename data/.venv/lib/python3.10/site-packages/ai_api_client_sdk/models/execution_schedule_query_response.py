from typing import Any, Dict, List

from .base_models import QueryResponse
from .execution_schedule import ExecutionSchedule


class ExecutionScheduleQueryResponse(QueryResponse):
    """The ExecutionScheduleQueryResponse object defines the response of the execution schedule query request
    :param resources: List of the execution schedules returned from the server
    :type resources: List[class:`ai_api_client_sdk.models.execution_schedule.ExecutionSchedule`]
    :param count: Total number of the queried execution schedules
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, resources: List[ExecutionSchedule], count: int, **kwargs):
        super().__init__(resources=resources, count=count, **kwargs)

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.execution_schedule_query_response.ExecutionScheduleQueryResponse`
        object, created from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.execution_schedule_query_response.ExecutionScheduleQueryResponse`
        """
        response_dict['resources'] = [ExecutionSchedule.from_dict(r) for r in response_dict['resources']]
        return ExecutionScheduleQueryResponse(**response_dict)
