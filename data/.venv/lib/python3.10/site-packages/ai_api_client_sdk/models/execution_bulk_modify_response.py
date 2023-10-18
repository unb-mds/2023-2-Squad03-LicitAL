from typing import List, Union, Dict
from .base_models import BasicResponse, BulkModifyErrorResponse


class ExecutionBulkModifyResponse:
    """The ExecutionBulkModifyResponse object defines the response to the executions bulk modify request
    :param exeuctions: Response to the bulk modify request of executions
    :type exeuctions: List[Union[BasicResponse, BulkModifyErrorResponse]]
    """
    def __init__(self, executions: List[Union[BasicResponse, BulkModifyErrorResponse]], **kwargs):
        self.executions: List[Union[BasicResponse, BulkModifyErrorResponse]] = executions

    def __str__(self):
        ebmr_str = ''
        for d in self.executions:
            ebmr_str += f'{d.__str__()}\n'
        return ebmr_str

    @staticmethod
    def from_dict(response_dict: Dict[str, List[Dict[str, Union[str, Dict]]]]):
        """Returns a :class:`ai_api_client_sdk.models.execution_bulk_modify_response.ExecutionBulkModifyResponse` object,
        created from the values provided as parameter

        :param response_dict: Which includes the necessary values to create the object
        :type response_dict: Dict[str, List[Dict[str, Union[str, Dict]]]]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.execution_bulk_modify_response.ExecutionBulkModifyResponse`
        """
        response_dict['executions'] = [
            BulkModifyErrorResponse.from_dict(d) if 'error' in d else BasicResponse.from_dict(d)
            for d in response_dict['executions']
        ]

        return ExecutionBulkModifyResponse(**response_dict)
