# pylint: disable=C0114
from typing import List, Callable
import os

from ai_core_sdk.helpers import Authenticator, is_within_aicore
from ai_core_sdk.models import Metric, MetricCustomInfo, MetricTag, MetricsQueryResponse
from ai_core_sdk.resource_clients import AIAPIV2Client, RestClient
from ai_core_sdk.exception import AIAPIAuthenticatorException
from ai_core_sdk.resource_clients.metrics_client import MetricsCoreClient


class Tracking(MetricsCoreClient): # pylint: disable=W0223
    """Tracking is a class implemented for interacting with the metrics related
    endpoints of the server. It is a wrapper around the base class
    :class:`ai_core_sdk.resource_clients.metrics_client.MetricsCoreClient`

    :param base_url: Base URL of the AI Core. Should include the base path as well. (i.e., "<base_url>/lm/scenarios"
    should work)
    :type base_url: str
    :param auth_url: URL of the authorization endpoint. Should be the full URL (including /oauth/token), defaults to
        None
    :type auth_url: str, optional
    :param client_id: client id to be used for authorization, defaults to None
    :type client_id: str, optional
    :param client_secret: client secret to be used for authorization, defaults to None
    :type client_secret: str, optional
    :param token_creator: the function which returns the Bearer token, when called. Either this, or
        auth_url & client_id & client_secret should be specified, defaults to None
    :type token_creator: Callable[[], str], optional
    :param resource_group: The default resource group which will be used while sending the requests to the server. If
        not set, the resource_group should be specified with every request to the server, defaults to None
    :type resource_group: str, optional
    """
    def __init__(self, base_url: str = None, auth_url: str = None, client_id: str = None, client_secret: str = None, # pylint: disable=W0231,R0913
                 token_creator: Callable[[], str] = None, resource_group: str = None):
        self.base_url: str = base_url
        self.metrics_path = '/metrics'
        self.local_experimentation = False
        ai_api_base_url = f'{base_url}/lm'

        if base_url:
            if not token_creator:
                if not (auth_url and client_id and client_secret):
                    raise AIAPIAuthenticatorException(
                        'Either token_creator or auth_url & client_id & client_secret should be provided')
                token_creator = Authenticator(auth_url=auth_url,
                                              client_id=client_id,
                                              client_secret=client_secret).get_token
            ai_api_v2_client  = AIAPIV2Client(base_url=ai_api_base_url, auth_url=auth_url, token_creator=token_creator,
                                         resource_group=resource_group)
            self.metrics_core_client = MetricsCoreClient(rest_client = ai_api_v2_client.rest_client)
        elif is_within_aicore():
            api_base_url = os.getenv('AICORE_TRACKING_ENDPOINT')
            # framing the base url of tracking endpoint
            base_url = f'{api_base_url}/api/v1'
            # dummy token creator function to be passed to rest client
            def dummy_token_creator():
                return ''
            token_creator = dummy_token_creator
            # resource group will be auto detected from the request going to tracking api from the training pod.
            # Hence not passing the resource group id
            resource_group = ''
            rest_client: RestClient = RestClient(base_url=base_url, get_token=token_creator,
                                                  resource_group=resource_group)
            self.metrics_core_client = MetricsCoreClient(rest_client = rest_client,
                                                         execution_id=os.getenv('AICORE_EXECUTION_ID'))
        else:
            print('Warning: Enabling local experimentation. Metrics logged will not be persisted anywhere.')
            self.local_experimentation = True

    def modify(self, execution_id: str = '', metrics: List[Metric] = None, tags: List[MetricTag] = None, # pylint: disable=R0913
               custom_info: List[MetricCustomInfo] = None, resource_group: str = None) -> None:
        """Creates or updates the metrics for an execution.

        :param execution_id: ID of the execution, of which the metrics should be modified.
        :type execution_id: str
        :param metrics: List of the metrics related to the execution, defaults to None
        :type metrics: List[class:`ai_api_client_sdk.metric.Metric`], optional
        :param tags: List of the tags related to the execution, defaults to None
        :type tags: List[class:'ai_api_client_sdk.models.metric_tag.MetricTag'], optional
        :param custom_info: List of custom info related to the execution, defaults to None
        :type custom_info: List[class:`ai_api_client_sdk.models.metric_custom_info.MetricCustomInfo`], optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
    server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        """
        if not self.local_experimentation:
            self.metrics_core_client.modify(execution_id=execution_id, metrics=metrics, tags=tags,
               custom_info=custom_info, resource_group=resource_group)

    def log_metrics(self, metrics: List[Metric], execution_id: str = '', artifact_name: str = None,
                    resource_group: str = None) -> None:
        """Creates or updates the metrics for an execution.

        :param metrics: List of the metrics related to the execution,
        :type metrics: List[class:`ai_api_client_sdk.metric.Metric`]
        :param execution_id: ID of the execution, of which the metrics should be modified.
        :type execution_id: str
        :param artifact_name: Name of the artifact to associate with a metric, defaults to None
        :type artifact_name: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
    server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        """
        if not self.local_experimentation:
            self.metrics_core_client.log_metrics(metrics=metrics,
                                                 execution_id=execution_id,
                                                 artifact_name=artifact_name,
                                                 resource_group=resource_group)

    def set_custom_info(self, custom_info: List[MetricCustomInfo], execution_id: str = '',
                        resource_group: str = None) -> None:
        """log custom info against the given execution
        captures consumption semantics for the metrics or complex metric in JSON format.


        :param custom_info: List of custom info related to the execution
        :type custom_info: List[class:`ai_api_client_sdk.models.metric_custom_info.MetricCustomInfo`], optional
        :param execution_id: ID of the execution, of which the metrics should be modified.
        :type execution_id: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
    server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        """
        if not self.local_experimentation:
            self.metrics_core_client.set_custom_info(custom_info=custom_info, execution_id=execution_id,
                        resource_group=resource_group)

    def set_tags(self, tags: List[MetricTag], execution_id: str = '', resource_group: str = None) -> None:
        """log tags against the given execution

        :param tags: List of the tags related to the execution, defaults to None
        :type tags: List[class:'ai_api_client_sdk.models.metric_tag.MetricTag']
        :param execution_id: ID of the execution, of which the metrics should be modified.
        :type execution_id: str
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
    server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        """
        if not self.local_experimentation:
            self.metrics_core_client.set_tags(tags=tags, execution_id=execution_id, resource_group=resource_group)

    def query(self, filter: str = None, execution_ids: List[str] = None, # pylint: disable=W0622
              select: List[str] = None, resource_group: str = None) -> \
            MetricsQueryResponse:
        """Creates or updates the metrics for an execution.

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
        if self.local_experimentation:
            print('Warning: Response will be always empty')
            return MetricsQueryResponse.from_dict({"count":0,"resources":[]})
        return self.metrics_core_client.query(filter=filter,
                                              execution_ids=execution_ids,
                                              select=select,
                                              resource_group=resource_group)

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
        if not self.local_experimentation:
            self.metrics_core_client.delete(execution_id=execution_id, resource_group=resource_group)
