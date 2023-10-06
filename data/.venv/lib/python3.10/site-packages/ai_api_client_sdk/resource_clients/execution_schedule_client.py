from datetime import datetime

from ai_api_client_sdk.helpers.datetime_parser import DATETIME_FORMAT
from ai_api_client_sdk.models.base_models import BasicResponse
from ai_api_client_sdk.models.execution_schedule import ExecutionSchedule
from ai_api_client_sdk.models.execution_schedule_create_response import ExecutionScheduleCreateResponse
from ai_api_client_sdk.models.execution_schedule_query_response import ExecutionScheduleQueryResponse
from ai_api_client_sdk.models.status import ScheduleStatus
from ai_api_client_sdk.resource_clients.base_client import BaseClient
from ai_api_client_sdk.exception import AIAPIInvalidInputException


class ExecutionScheduleClient(BaseClient):
    """ExecutionScheduleClient is a class implemented for interacting with the execution schedules related endpoints of
    the server. It implements the base class :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """

    def create(self, name: str, cron: str, configuration_id: str, start: datetime = None, end: datetime = None,
               resource_group: str = None) -> ExecutionScheduleCreateResponse:
        """Creates an execution schedule.

        :param name: Name of the execution schedule
        :type name: str
        :param cron: Cron defining the schedule to run the executions
        :type name: str
        :param configuration_id: ID of the configuration for the execution schedule
        :type configuration_id: str
        :param start: Start time of the execution schedule in UTC, defaults to None
        :type start: datetime, optional
        :param end: End time of the execution schedule in UTC e.g., defaults to None
        :type end: datetime, optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.execution_schedule_create_response.ExecutionScheduleCreateResponse`
        """
        body = {
            "name": name,
            "cron": cron,
            "configuration_id": configuration_id,
        }
        if start:
            body['start'] = start.strftime(DATETIME_FORMAT)
        if end:
            body['end'] = end.strftime(DATETIME_FORMAT)
        response_dict = self.rest_client.post(path='/executionSchedules', body=body, resource_group=resource_group)

        return ExecutionScheduleCreateResponse.from_dict(response_dict)

    def delete(self, execution_schedule_id: str, resource_group: str = None) -> BasicResponse:
        """Deletes the execution schedule.

        :param execution_schedule_id: ID of the execution schedule to be deleted
        :type execution_schedule_id: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIPreconditionFailedException` if a 412 response is received from
            the server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.base_models.BasicResponse`
        """
        response_dict = self.rest_client.delete(path=f'/executionSchedules/{execution_schedule_id}',
                                                resource_group=resource_group)
        return BasicResponse.from_dict(response_dict)

    def get(self, execution_schedule_id: str, resource_group: str = None) -> ExecutionSchedule:
        """Retrieves the execution schedule from the server.

        :param execution_schedule_id: ID of the execution schedule to be retrieved
        :type execution_schedule_id: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: The retrieved execution
        :rtype: class:`ai_api_client_sdk.models.execution.Execution`
        """
        execution_schedule_dict = self.rest_client.get(path=f'/executionSchedules/{execution_schedule_id}',
                                                       resource_group=resource_group)
        return ExecutionSchedule.from_dict(execution_schedule_dict)

    def modify(self, execution_schedule_id: str, cron: str = None, start: datetime = None, end: datetime = None,
               configurationId: str = None, status: ScheduleStatus = None, resource_group: str = None) -> BasicResponse:
        """Modifies the execution schedule.

        :param execution_schedule_id: ID of the execution to be modified
        :type execution_schedule_id: str
        :param cron: Cron defining the schedule to run the executions, defaults to None
        :type cron: str, optional
        :param configurationId: ID of the configuration for the execution schedule, defaults to None
        :type configurationId: str, optional
        :param start: Start time of the execution schedule in UTC, defaults to None
        :type start: datetime, optional
        :param end: End time of the execution schedule in UTC, defaults to None
        :type end: datetime, optional
        :param status: pause / resume Status of the execution schedule, defaults to None
        :type status: class:`ai_api_client_sdk.models.status.ScheduleStatus`, optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.base_models.BasicResponse`
        """
        body = {}
        if cron:
            body['cron'] = cron
        if start:
            body['start'] = start.strftime(DATETIME_FORMAT)
        if end:
            body['end'] = end.strftime(DATETIME_FORMAT)
        if configurationId:
            body['configurationId'] = configurationId
        if status:
            body['status'] = status.value

        if not body:
            raise AIAPIInvalidInputException('The Request Body cannot be empty.')

        response_dict = self.rest_client.patch(path=f'/executionSchedules/{execution_schedule_id}', body=body,
                                               resource_group=resource_group)
        return BasicResponse.from_dict(response_dict)

    def query(self, configuration_id: str = None, status: ScheduleStatus = None, top: int = None,
              skip: int = None, resource_group: str = None) -> ExecutionScheduleQueryResponse:
        """Queries the execution schedules.

        :param configuration_id: ID of the configuration, the executions should be configured by, defaults to None
        :type configuration_id: str, optional
        :param status:  ScheduleStatus which the execution schedule should currently have
        :type status: class:`ai_api_client_sdk.models.schedule_status.ScheduleStatus`, optional
        :param top: Number of executions to be retrieved, defaults to None
        :type top: int, optional
        :param skip: Number of executions to be skipped, from the list of the queried executions, defaults to None
        :type skip: int, optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.execution_query_response.ExecutionQueryResponse`
        """
        params = self._form_query_params(configuration_id=configuration_id,
                                         status=status.value if status else None,
                                         top=top, skip=skip)
        response_dict = self.rest_client.get(path='/executionSchedules', params=params, resource_group=resource_group)
        return ExecutionScheduleQueryResponse.from_dict(response_dict)

    def count(self, configuration_id: str = None, status: ScheduleStatus = None,
              resource_group: str = None) -> int:
        """Counts the number of executions schedules.

        :param configuration_id: ID of the configuration, the executions should be configured by, defaults to None
        :type configuration_id: str, optional
        :param status: ScheduleStatus which the execution schedule should currently have, defaults to None
        :type status: class:`ai_api_client_sdk.models.schedule_status.ScheduleStatus`, optional
        :param resource_group: Resource group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: int
        """
        params = self._form_query_params(configuration_id=configuration_id,
                                         status=status.value if status else None)
        return self.rest_client.get(path='/executionSchedules/$count', params=params, resource_group=resource_group)
