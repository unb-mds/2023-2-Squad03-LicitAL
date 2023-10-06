from datetime import datetime
from typing import List, Union
import re

from ai_api_client_sdk.exception import AIAPIInvalidInputException
from ai_api_client_sdk.models.base_models import BasicResponse, Order, BasicModifyRequest
from ai_api_client_sdk.models.deployment import Deployment
from ai_api_client_sdk.models.deployment_create_response import DeploymentCreateResponse
from ai_api_client_sdk.models.deployment_query_response import DeploymentQueryResponse
from ai_api_client_sdk.models.deployment_bulk_modify_response import DeploymentBulkModifyResponse
from ai_api_client_sdk.models.deployment_get_status_response import DeploymentGetStatusResponse
from ai_api_client_sdk.models.log_response import LogResponse
from ai_api_client_sdk.models.status import Status
from ai_api_client_sdk.models.target_status import TargetStatus
from ai_api_client_sdk.resource_clients.base_client import BaseClient


class DeploymentClient(BaseClient):
    """DeploymentClient is a class implemented for interacting with the deployment related endpoints of the server. It
    implements the base class :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """

    def create(self, configuration_id: str, ttl: str = None, resource_group: str = None) -> DeploymentCreateResponse:
        """Creates a deployment.

        :param configuration_id: ID of the configuration, that should configure the deployment
        :type configuration_id: str
        :param ttl: Time to live for deployment and can be none or take  a number followed by the unit
        (any of following values, minutes(m|M), hours(h|H) or days(d|D))
        :type ttl: str, optional
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
        :rtype: class:`ai_api_client_sdk.models.deployment_create_response.DeploymentCreateResponse`
        """
        body = {"configuration_id": configuration_id}
        if ttl:
            body['ttl'] = ttl
        response_dict = self.rest_client.post(path='/deployments', body=body,
                                              resource_group=resource_group)
        return DeploymentCreateResponse.from_dict(response_dict)

    def delete(self, deployment_id: str, resource_group: str = None) -> BasicResponse:
        """Deletes the deployment.

        :param deployment_id: ID of the deployment to be deleted
        :type deployment_id: str
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
        response_dict = self.rest_client.delete(f'/deployments/{deployment_id}', resource_group=resource_group)
        return BasicResponse.from_dict(response_dict)

    def get(self, deployment_id: str, resource_group: str = None, select: str = None) -> \
            Union[Deployment, DeploymentGetStatusResponse]:
        """Retrieves the deployment from the server.

        :param deployment_id: ID of the deployment to be retrieved
        :type deployment_id: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :param select: only status supported. Get deployment for a given deployment id and select status
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
        :return: The retrieved deployment
        :rtype: class:Union[`ai_api_client_sdk.models.deployment.Deployment`,
            `ai_api_client_sdk.models.deployment_get_status_response.DeploymentGetStatusResponse`]
        """
        if select and 'status' in select:
            param = self._form_query_params(select='status')
            deployment_dict = self.rest_client.get(path=f'/deployments/{deployment_id}',  params=param,
                                                   resource_group=resource_group)
            return DeploymentGetStatusResponse.from_dict(deployment_dict)
        else:
            deployment_dict = self.rest_client.get(path=f'/deployments/{deployment_id}', resource_group=resource_group)
            return Deployment.from_dict(deployment_dict)

    def modify(self, deployment_id: str, target_status: TargetStatus = None, configuration_id: str = None,
               resource_group: str = None) -> BasicResponse:
        """Modifies the deployment, by changing either the target status, or the configuration ID.

        :param deployment_id: ID of the deployment to be modified
        :type deployment_id: str
        :param target_status: Desired target status of the deployment, defaults to None
        :type target_status: class:`ai_api_client_sdk.models.target_status.TargetStatus`, optional
        :param configuration_id: ID of the new configuration to be used by the deployment, defaults to None
        :type configuration_id: str, optional
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
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.base_models.BasicResponse`
        """
        body = {}
        if target_status and configuration_id:
            raise AIAPIInvalidInputException(
                'Either target_status or configuration_id should be provided as input, not both')
        if target_status:
            body['target_status'] = target_status.value
        elif configuration_id:
            body['configuration_id'] = configuration_id
        response_dict = self.rest_client.patch(path=f'/deployments/{deployment_id}', body=body,
                                               resource_group=resource_group)
        return BasicResponse.from_dict(response_dict)

    def query(self, scenario_id: str = None, configuration_id: str = None, executable_ids: List[str] = None,
              status: Status = None, top: int = None, skip: int = None,
              resource_group: str = None) -> DeploymentQueryResponse:
        """Queries the deployments.

        :param scenario_id: ID of the scenario the deployments should belong to, defaults to None
        :type scenario_id: str, optional
        :param configuration_id: ID of the configuration, the deployments should be configured by, defaults to None
        :type configuration_id: str, optional
        :param executable_ids: IDs of the executables the deployments should be created from, defaults to None
        :type executable_ids: List[str], optional
        :param status: Status which the deployments should currently have
        :type status: class:`ai_api_client_sdk.models.status.Status`, optional
        :param top: Number of deployments to be retrieved, defaults to None
        :type top: int, optional
        :param skip: Number of deployments to be skipped, from the list of the queried deployments, defaults to None
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
        :rtype: class:`ai_api_client_sdk.models.deployment_query_response.DeploymentQueryResponse`
        """
        params = self._form_query_params(scenario_id=scenario_id, configuration_id=configuration_id,
                                         executable_ids=executable_ids, status=status.value if status else None,
                                         top=top, skip=skip)
        response_dict = self.rest_client.get(path='/deployments', params=params, resource_group=resource_group)
        return DeploymentQueryResponse.from_dict(response_dict)

    def count(self, scenario_id: str = None, configuration_id: str = None, executable_ids: List[str] = None,
              status: Status = None, resource_group: str = None) -> int:
        """Counts the number of deployments.

        :param scenario_id: ID of the scenario, the deployments should belong to, defaults to None
        :type scenario_id: str, optional
        :param configuration_id: ID of the configuration, the deployments should be configured by, defaults to None
        :type configuration_id: str, optional
        :param executable_ids: IDs of the executables, the deployments should be created from, defaults to None
        :type executable_ids: List[str], optional
        :param status: Status which the deployments should currently have
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
                                         executable_ids=executable_ids, status=status.value if status else None)
        return self.rest_client.get(path='/deployments/$count', params=params, resource_group=resource_group)

    def query_logs(self, deployment_id: str, top: int = None, start: datetime = None, end: datetime = None,
                   order: Order = None, resource_group: str = None) -> LogResponse:
        """Queries the logs of the deployment.

        :param deployment_id: ID of the deployment
        :type deployment_id: str
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
        params = self._form_query_params(top=top, start=start, end=end, order=order)
        response_dict = self.rest_client.get(path=f'/deployments/{deployment_id}/logs', params=params,
                                             resource_group=resource_group)
        return LogResponse.from_dict(response_dict)

    def bulk_modify(self, deployments: List[BasicModifyRequest],
                    resource_group: str = None) -> DeploymentBulkModifyResponse:
        """Modifies the deployments
        :param deployments: List of deployment modify requests
        :type deployments: List[DeploymentModifyRequest]
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
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.deployment_bulk_modify_response.DeploymentBulkModifyResponse`
        """
        body = {'deployments': [bmr.to_dict() for bmr in deployments]}
        response_dict = self.rest_client.patch(path='/deployments', body=body, resource_group=resource_group)
        return DeploymentBulkModifyResponse.from_dict(response_dict)        
