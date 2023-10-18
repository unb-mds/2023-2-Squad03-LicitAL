from datetime import datetime
from typing import Any, Dict

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime
from ai_api_client_sdk.models.enactment_get_status_response import EnactmentGetStatusResponse
from ai_api_client_sdk.models.status import Status


class ExecutionGetStatusResponse(EnactmentGetStatusResponse):
    """The ExecutionGetStatusResponse object defines the response of the execution get status
    :param id: ID of the execution
    :type id: str
    :param configuration_id: ID of the configuration which configured the execution
    :type configuration_id: str
    :param status: Status of the execution
    :type status: class:`ai_api_client_sdk.models.status.Status`
    :param created_at: Time when the execution was created
    :type created_at: datetime
    :param modified_at: Time when the execution was last modified
    :type modified_at: datetime
    :param status_details: A dict, which gives detailed information about the status of the execution, defaults to None
    :type status_details: Dict[str, Any], optional
    """
    def __init__(self, id: str, configuration_id: str,
                 status: Status, created_at: datetime, modified_at: datetime, status_details: Dict[str, Any] = None):
        super().__init__(id=id, configuration_id=configuration_id, status=status, created_at=created_at,
                         modified_at=modified_at, status_details=status_details)

    def __str__(self):
        return "Execution id: " + str(self.id)

    @staticmethod
    def from_dict(execution_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.execution_get_status_response.ExecutionGetStatusResponse` object,
         created from the values in the dict provided as parameter
        :param execution_dict: Dict which includes the necessary values to create the object
        :type execution_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.execution_get_status_response.ExecutionGetStatusResponse`
        """
        execution_dict['status'] = Status(execution_dict['status'])
        execution_dict['created_at'] = parse_datetime(execution_dict['created_at'])
        execution_dict['modified_at'] = parse_datetime(execution_dict['modified_at'])
        return ExecutionGetStatusResponse(**execution_dict)
