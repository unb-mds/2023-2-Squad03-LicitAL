from typing import List
import warnings

from ai_api_client_sdk.models.metrics_query_response import MetricsQueryResponse
from ai_api_client_sdk.resource_clients.base_client import BaseClient


class MetricsClient(BaseClient):
    """MetricsClient is a class implemented for interacting with the metrics related endpoints of the server. It
    implements the base class :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """

    def query(self, filter: str = None, execution_ids: List[str] = None, select: List[str] = None, resource_group: str = None) -> \
            MetricsQueryResponse:
        """Queries the metrics.

        :param filter: Deprecated. Use parameter execution_ids instead. A filter expression that filters the metric
            resources using execution IDs. User can only use in, eq operators in filter expression, defaults to None
        :type filter: str, optional
        :param execution_ids: IDs of the executions, of which the metrics should be retrieved, defaults to None
        :type execution_ids: List[str], optional
        :param select: Values of select can be metrics,tags,customInfo or any of the combinations of these or *. 
            Can be used to select(project) only the resources specified
        :type select: List[str], optional
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
        :rtype: class:`ai_api_client_sdk.models.metrics_query_response.MetricsQueryResponse`
        """
        params = self._form_query_params(filter=filter, execution_ids=execution_ids, select=select)
        if params and 'filter' in params:  # pylint: disable=unsupported-membership-test
            warnings.warn('Parameter filter is deprecated. Use parameter execution_ids instead.', DeprecationWarning, stacklevel=2)
            params['$filter'] = params['filter']  # pylint: disable=unsupported-assignment-operation,unsubscriptable-object
            del params['filter']  # pylint: disable=unsupported-delete-operation
        response_dict = self.rest_client.get(path='/metrics', params=params, resource_group=resource_group)
        return MetricsQueryResponse.from_dict(response_dict)

    def delete(self, execution_id: str, resource_group: str = None) -> None:
        """Deletes the metrics.

        :param execution_id: ID of the execution, of which the metrics should be deleted.
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
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        """
        params = self._form_query_params(execution_id=execution_id)
        self.rest_client.delete(path='/metrics', params=params, resource_group=resource_group)
