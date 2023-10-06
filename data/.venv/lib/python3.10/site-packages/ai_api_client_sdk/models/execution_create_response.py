from typing import Any, Dict

from .base_models import BasicResponse
from .status import Status


class ExecutionCreateResponse(BasicResponse):
    """The ExecutionCreateResponse object defines the response of the execution create request
    :param id: ID of the execution
    :type id: str
    :param message: Response message from the server
    :type message: str
    :param status: Status of the execution
    :type status: class:`ai_api_client_sdk.models.status.Status`
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, message: str, status: Status, **kwargs):
        super().__init__(id=id, message=message, **kwargs)
        self.status: Status = status

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.execution_create_response.ExecutionCreateResponse` object,
        created from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.execution_create_response.ExecutionCreateResponse`
        """
        response_dict['status'] = Status(response_dict['status'])
        return ExecutionCreateResponse(**response_dict)
