from typing import List

from ai_core_sdk.models import Metric, MetricCustomInfo, MetricTag, MetricLabel
from ai_core_sdk.resource_clients import MetricsClient

from ai_core_sdk.exception import AICoreSDKException
class MetricsCoreClient(MetricsClient):
    """MetricsCoreClient is a class implemented for interacting with the metrics related
    endpoints of the server. It is inherited from the base class
    :class:`ai_api_client_sdk.resource_clients.metrics_client.MetricsClient`
    """

    def __init__(self, rest_client, execution_id: str = None) -> None:
        super().__init__(rest_client)
        self.execution_id = execution_id
        self.rest_client = rest_client
        self.metrics_path = '/metrics'

    def modify(self, execution_id: str = '', metrics: List[Metric] = None, tags: List[MetricTag] = None,
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
        body = {'execution_id':  self.execution_id if self.execution_id else execution_id}
        if metrics:
            body['metrics'] = [metric.to_dict() for metric in metrics]
        if tags:
            body['tags'] = [tag.__dict__ for tag in tags]
        if custom_info:
            body['custom_info'] = [c_info.__dict__ for c_info in custom_info]

        self.rest_client.patch(path=self.metrics_path, body=body, resource_group=resource_group)

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
        body = {'execution_id':  self.execution_id if self.execution_id else execution_id}
        if artifact_name is not None:
            if not isinstance(artifact_name, str):
                raise AICoreSDKException('Artifact name of type string is expected')

            artifact_label = {
                'name': "metrics.ai.sap.com/Artifact.name",
                'value': artifact_name
            }

            for metric in metrics:
                if not metric.labels:
                    metric.labels = [MetricLabel.from_dict(artifact_label)]
                else:
                    metric.labels.append(MetricLabel.from_dict(artifact_label))
        if metrics:
            body['metrics'] = [metric.to_dict() for metric in metrics]
        self.rest_client.patch(path=self.metrics_path, body=body, resource_group=resource_group)

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
        body = {'execution_id':  self.execution_id if self.execution_id else execution_id}
        if custom_info:
            body['custom_info'] = [c_info.__dict__ for c_info in custom_info]
        self.rest_client.patch(path=self.metrics_path, body=body, resource_group=resource_group)

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
        body = {'execution_id':  self.execution_id if self.execution_id else execution_id}
        if tags:
            body['tags'] = [tag.__dict__ for tag in tags]
        self.rest_client.patch(path=self.metrics_path, body=body, resource_group=resource_group)
