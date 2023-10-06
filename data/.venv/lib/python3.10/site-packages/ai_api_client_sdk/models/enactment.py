from datetime import datetime
from typing import Any, Dict

from ai_api_client_sdk.models.status import Status
from ai_api_client_sdk.models.target_status import TargetStatus


class Enactment:
    """Enactment object is base class for Execution/Deployment, defining their common attributes

    :param id: ID of the enactment
    :type id: str
    :param configuration_id: ID of the configuration which configured the enactment
    :type configuration_id: str
    :param configuration_name: Name of the configuration which configured the enactment
    :type configuration_name: str
    :param scenario_id: ID of the scenario which the enactment belongs to
    :type scenario_id: str
    :param status: Status of the enactment
    :type status: class:`ai_api_client_sdk.models.status.Status`
    :param target_status: Target status of the enactment
    :type target_status: class:`ai_api_client_sdk.models.target_status.TargetStatus`
    :param created_at: Time when the enactment was created
    :type created_at: datetime
    :param modified_at: Time when the enactment was last modified
    :type modified_at: datetime
    :param status_message: A string, which gives information about the status of the enactment, defaults to None
    :type status_message: str, optional
    :param status_details: A dict, which gives detailed information about the status of the enactment, defaults to None
    :type status_details: Dict[str, Any], optional
    :param submission_time: Time when the enactment was submitted
    :type submission_time: datetime, optional
    :param start_time: Time when the enactment status changed to RUNNING
    :type start_time: datetime, optional
    :param completion_time: Time when the enactment status changed to COMPLETED/DEAD/STOPPED
    :type completion_time: datetime, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, configuration_id: str, configuration_name, scenario_id: str, status: Status,
                 target_status: TargetStatus, created_at: datetime, modified_at: datetime, status_message: str = None,
                 status_details: Dict[str, Any] = None, submission_time: datetime = None, start_time: datetime = None,
                 completion_time: datetime = None, **kwargs):
        self.id: str = id
        self.configuration_id: str = configuration_id
        self.configuration_name: str = configuration_name
        self.scenario_id: str = scenario_id
        self.status: Status = status
        self.target_status: TargetStatus = target_status
        self.created_at: datetime = created_at
        self.modified_at: datetime = modified_at
        self.status_message: str = status_message
        self.status_details: Dict[str, Any] = status_details
        self.submission_time: datetime = submission_time
        self.start_time: datetime = start_time
        self.completion_time: datetime = completion_time

    def __str__(self):
        return "Enactment id: " + str(self.id)
