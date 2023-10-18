from typing import List, Union
from datetime import datetime

from ai_api_client_sdk.models.base_models import BasicResponse, Order, BasicModifyRequest
from ai_api_client_sdk.models.execution import Execution
from ai_api_client_sdk.models.execution_create_response import ExecutionCreateResponse
from ai_api_client_sdk.models.execution_query_response import ExecutionQueryResponse
from ai_api_client_sdk.models.execution_get_status_response import ExecutionGetStatusResponse
from ai_api_client_sdk.models.execution_bulk_modify_response import ExecutionBulkModifyResponse
from ai_api_client_sdk.models.log_response import LogResponse
from ai_api_client_sdk.models.status import Status
from ai_api_client_sdk.models.target_status import TargetStatus
from ai_api_client_sdk.resource_clients.base_client import BaseClient


class ExecutionClient(BaseClient):
    """ExecutionClient is a class implemented for interacting with the execution related endpoints of the server. It
    implements the base class :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """

    def create(self, configuration_id: str, resource_group: str = None) -> ExecutionCreateResponse:
        """Creates an execution.

        :param configuration_id: ID of the configuration, that should configure the execution
        :type configuration_id: str
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
        :rtype: class:`ai_api_client_sdk.models.execution_create_response.ExecutionCreateResponse`
        """
        body = {"configuration_id": configuration_id}
        response_dict = self.rest_client.post(path='/executions', body=body,
                                              resource_group=resource_group)
        return ExecutionCreateResponse.from_dict(response_dict)

    def delete(self, execution_id: str, resource_group: str = None) -> BasicResponse:
        """Deletes the execution.

        :param execution_id: ID of the execution to be deleted
        :type execution_id: str
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
        response_dict = self.rest_client.delete(path=f'/executions/{execution_id}', resource_group=resource_group)
        return BasicResponse.from_dict(response_dict)

    def get(self, execution_id: str, resource_group: str = None, select: str = None) -> \
            Union[Execution, ExecutionGetStatusResponse]:
        """Retrieves the execution from the server.

        :param execution_id: ID of the execution to be retrieved
        :type execution_id: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :param select: only status supported. Get execution for a given execution id and select status
        :type select: str, optional
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
        :rtype: class:Union[`ai_api_client_sdk.models.execution.Execution`,
            `ai_api_client_sdk.models.execution_get_status_response.ExecutionGetStatusResponse`]
        """
        if select and 'status' in select:
            param = self._form_query_params(select='status')
            execution_dict = self.rest_client.get(path=f'/executions/{execution_id}', params=param,
                                                  resource_group=resource_group)
            return ExecutionGetStatusResponse.from_dict(execution_dict)
        else:
            execution_dict = self.rest_client.get(path=f'/executions/{execution_id}', resource_group=resource_group)
            return Execution.from_dict(execution_dict)

    def modify(self, execution_id: str, target_status: TargetStatus, resource_group: str = None) -> BasicResponse:
        """Modifies the execution, by changing the target status.

        :param execution_id: ID of the execution to be modified
        :type execution_id: str
        :param target_status: Desired target status of the execution, defaults to None
        :type target_status: class:`ai_api_client_sdk.models.target_status.TargetStatus`, optional
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
        body = {'target_status': target_status.value}
        response_dict = self.rest_client.patch(path=f'/executions/{execution_id}', body=body,
                                               resource_group=resource_group)
        return BasicResponse.from_dict(response_dict)

    def query(self, scenario_id: str = None, configuration_id: str = None, executable_ids: List[str] = None,
              execution_schedule_id: str = None, status: Status = None, top: int = None, skip: int = None,
              resource_group: str = None) -> ExecutionQueryResponse:
        """Queries the executions.

        :param scenario_id: ID of the scenario the executions should belong to, defaults to None
        :type scenario_id: str, optional
        :param configuration_id: ID of the configuration, the executions should be configured by, defaults to None
        :type configuration_id: str, optional
        :param executable_ids: IDs of the executables the executions should be created from, defaults to None
        :type executable_ids: List[str], optional
        :param execution_schedule_id: ID of the execution schedule, defaults to None
        :type execution_schedule_id: str, optional
        :param status: Status which the executions should currently have
        :type status: class:`ai_api_client_sdk.models.status.Status`, optional
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
        params = self._form_query_params(scenario_id=scenario_id, configuration_id=configuration_id,
                                         executable_ids=executable_ids, execution_schedule_id=execution_schedule_id,
                                         status=status.value if status else None,
                                         top=top, skip=skip)
        response_dict = self.rest_client.get(path='/executions', params=params, resource_group=resource_group)
        return ExecutionQueryResponse.from_dict(response_dict)

    def count(self, scenario_id: str = None, configuration_id: str = None, executable_ids: List[str] = None,
              execution_schedule_id: str = None, status: Status = None, resource_group: str = None) -> int:
        """Counts the number of executions.

        :param scenario_id: ID of the scenario, the executions should belong to, defaults to None
        :type scenario_id: str, optional
        :param configuration_id: ID of the configuration, the executions should be configured by, defaults to None
        :type configuration_id: str, optional
        :param executable_ids: IDs of the executables, the executions should be created from, defaults to None
        :type executable_ids: List[str], optional
        :param execution_schedule_id: ID of the execution schedule, defaults to None
        :type execution_schedule_id: str, optional
        :param status: Status which the executions should currently have
        :type status: class:`ai_api_client_sdk.models.status.Status`, optional
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
        params = self._form_query_params(scenario_id=scenario_id, configuration_id=configuration_id,
                                         executable_ids=executable_ids, execution_schedule_id=execution_schedule_id,
                                         status=status.value if status else None)
        return self.rest_client.get(path='/executions/$count', params=params, resource_group=resource_group)

    def query_logs(self, execution_id: str, top: int = None, start: datetime = None, end: datetime = None,
                   order: Order = None, resource_group: str = None) -> LogResponse:
        """Queries the logs of the execution.

        :param execution_id: ID of the execution
        :type execution_id: str
        :param top: The max number of entries to return. Defaults to 1000. Limited to 5000 max.
        :type top: int
        :param start: The start time for the query. Defaults to one hour ago.
        :type start: datetime
        :param end: The end time for the query. Defaults to now.
        :type end: datetime
        :param order: Determines the sort order with respect to time. Defaults to asc.
        :type order: class:`ai_api_client_sdk.models.base_models.Order`
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
        :return: Logs from the execution
        :rtype: class:`ai_api_client_sdk.models.log_response.LogResponse`
        """
        params = self._form_query_params(
            top=top, start=start, end=end, order=order)
        response_dict = self.rest_client.get(path=f'/executions/{execution_id}/logs', params=params,
                                             resource_group=resource_group)
        return LogResponse.from_dict(response_dict)

    def bulk_modify(self, executions: List[BasicModifyRequest],
                    resource_group: str = None) -> ExecutionBulkModifyResponse:
        """Modifies the executions
        :param executions: List of execution modify requests
        :type executions: List[ExecutionModifyRequest]
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str, optional
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIPreconditionFailedException` if a 412 response is received from
            the server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.execution_bulk_modify_response.ExecutionBulkModifyResponse`
        """
        body = {'executions': [bmr.to_dict() for bmr in executions]}
        response_dict = self.rest_client.patch(path='/executions', body=body, resource_group=resource_group)
        return ExecutionBulkModifyResponse.from_dict(response_dict)
