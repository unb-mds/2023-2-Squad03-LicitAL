from datetime import datetime
from typing import Any, Dict

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime
from ai_api_client_sdk.models.status import ScheduleStatus


class ExecutionSchedule:
    """An Execution Schedule allows to trigger executions periodically

    :param id: ID of the execution schedule
    :type id: str
    :param name: Name of the execution schedule
    :type name: str
    :param cron: Cron defining the schedule to run the executions
    :type cron: str
    :param configuration_id: ID of the configuration for the execution schedule
    :type configuration_id: str
    :param status: status of the execution schedule
    :type status: str
    :param created_at: Time when the execution schedule was created
    :type created_at: datetime, optional
    :param modified_at: Time when the execution schedule was last modified
    :type modified_at: datetime, optional
    :param start: Start time of the execution schedule
    :type start: datetime, optional
    :param end: End time of the execution schedule
    :type end: datetime, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, name: str, cron: str, configuration_id: str, status: ScheduleStatus,
                 created_at: datetime, modified_at: datetime, start: datetime = None, end: datetime = None, **kwargs):
        self.id: str = id
        self.name = name
        self.cron: str = cron
        self.configuration_id: str = configuration_id
        self.status: ScheduleStatus = status
        self.start: datetime = start
        self.end: datetime = end
        self.created_at: datetime = created_at
        self.modified_at: datetime = modified_at

    def __str__(self):
        return "Execution Schedule id: " + str(self.id)

    @staticmethod
    def from_dict(execution_schedule_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.execution_schedule.Schedule` object, created from the values in
        the dict provided as parameter

        :param execution_schedule_dict: Dict which includes the necessary values to create the object
        :type execution_schedule_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.execution_schedule.Schedule`
        """
        execution_schedule_dict['status'] = ScheduleStatus(execution_schedule_dict['status'])
        execution_schedule_dict['created_at'] = parse_datetime(execution_schedule_dict['created_at'])
        execution_schedule_dict['modified_at'] = parse_datetime(execution_schedule_dict['modified_at'])
        if execution_schedule_dict.get('start'):
            execution_schedule_dict['start'] = parse_datetime(execution_schedule_dict['start'])
        if execution_schedule_dict.get('end'):
            execution_schedule_dict['end'] = parse_datetime(execution_schedule_dict['end'])
        return ExecutionSchedule(**execution_schedule_dict)
