from datetime import datetime
from typing import Any, Dict

from ai_api_client_sdk.models.status import Status
from ai_api_client_sdk.models.target_status import TargetStatus


class EnactmentGetStatusResponse:
    """EnactmentGetStatusResponse object defines the response from the server to get status of Execution/Deployment
    :param id: ID of the enactment
    :type id: str
    :param configuration_id: ID of the configuration which configured the enactment
    :type configuration_id: str
    :param status: Status of the enactment
    :type status: class:`ai_api_client_sdk.models.status.Status`
    :param created_at: Time when the enactment was created
    :type created_at: datetime
    :param modified_at: Time when the enactment was last modified
    :type modified_at: datetime
    :param status_details: A dict, which gives detailed information about the status of the enactment, defaults to None
    :type status_details: Dict[str, Any], optional
    """
    def __init__(self, id: str, configuration_id: str, status: Status,
                 created_at: datetime, modified_at: datetime, status_details: Dict[str, Any] = None):
        self.id: str = id
        self.configuration_id: str = configuration_id
        self.status: Status = status
        self.created_at: datetime = created_at
        self.modified_at: datetime = modified_at
        self.status_details: Dict[str, Any] = status_details

    def __str__(self):
        return "Enactment id: " + str(self.id)
