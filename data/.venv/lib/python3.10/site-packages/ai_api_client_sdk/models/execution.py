from datetime import datetime
from typing import Any, Dict, List

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime
from ai_api_client_sdk.models.artifact import Artifact
from ai_api_client_sdk.models.enactment import Enactment
from ai_api_client_sdk.models.status import Status
from ai_api_client_sdk.models.target_status import TargetStatus


class Execution(Enactment):
    """The Execution object defines an execution

    :param id: ID of the execution
    :type id: str
    :param configuration_id: ID of the configuration which configured the execution
    :type configuration_id: str
    :param configuration_name: Name of the configuration which configured the execution
    :type configuration_name: str
    :param scenario_id: ID of the scenario which the execution belongs to
    :type scenario_id: str
    :param status: Status of the execution
    :type status: class:`ai_api_client_sdk.models.status.Status`
    :param target_status: Target status of the execution
    :type target_status: class:`ai_api_client_sdk.models.target_status.TargetStatus`
    :param execution_schedule_id: ID of the execution schedule, defaults to None
    :type execution_schedule_id: str, optional
    :param created_at: Time when the execution was created
    :type created_at: datetime
    :param modified_at: Time when the execution was last modified
    :type modified_at: datetime
    :param output_artifacts: List of the artifacts created by the execution, defaults to None
    :type output_artifacts: List[class:`ai_api_client_sdk.models.artifact.Artifact`], optional
    :param status_message: Gives information about the status of the execution, defaults to None
    :type status_message: str, optional
    :param status_details: A dict, which gives detailed information about the status of the execution, defaults to None
    :type status_details: Dict[str, Any], optional
    :param submission_time: Time when the execution was submitted
    :type submission_time: datetime, optional
    :param start_time: Time when the execution status changed to RUNNING
    :type start_time: datetime, optional
    :param completion_time: Time when the execution status changed to COMPLETED/DEAD/STOPPED
    :type completion_time: datetime, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, configuration_id: str, configuration_name: str, scenario_id: str, status: Status,
                 target_status: TargetStatus, created_at: datetime, modified_at: datetime,
                 output_artifacts: List[Artifact] = None, status_message: str = None,
                 status_details: Dict[str, Any] = None, submission_time: datetime = None, start_time: datetime = None,
                 execution_schedule_id: str = None, completion_time: datetime = None, **kwargs):
        super().__init__(id=id, configuration_id=configuration_id, configuration_name=configuration_name,
                         scenario_id=scenario_id, status=status, target_status=target_status, created_at=created_at,
                         modified_at=modified_at, status_message=status_message, status_details=status_details,
                         submission_time=submission_time, start_time=start_time, completion_time=completion_time,
                         **kwargs)
        self.output_artifacts: List[Artifact] = output_artifacts
        self.execution_schedule_id = execution_schedule_id

    def __str__(self):
        return "Execution id: " + str(self.id)

    @staticmethod
    def from_dict(execution_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.execution.Execution` object, created from the values in the dict
        provided as parameter

        :param execution_dict: Dict which includes the necessary values to create the object
        :type execution_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.execution.Execution`
        """
        execution_dict['status'] = Status(execution_dict['status'])
        execution_dict['target_status'] = TargetStatus(execution_dict['target_status'])
        execution_dict['created_at'] = parse_datetime(execution_dict['created_at'])
        execution_dict['modified_at'] = parse_datetime(execution_dict['modified_at'])
        if execution_dict.get('submission_time'):
            execution_dict['submission_time'] = parse_datetime(execution_dict['submission_time'])
        if execution_dict.get('start_time'):
            execution_dict['start_time'] = parse_datetime(execution_dict['start_time'])
        if execution_dict.get('completion_time'):
            execution_dict['completion_time'] = parse_datetime(execution_dict['completion_time'])
        if execution_dict.get('output_artifacts'):
            execution_dict['output_artifacts'] = [Artifact.from_dict(oa) for oa in execution_dict['output_artifacts']]
        return Execution(**execution_dict)
