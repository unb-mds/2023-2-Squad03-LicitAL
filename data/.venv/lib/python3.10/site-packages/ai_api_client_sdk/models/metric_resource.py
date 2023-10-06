from typing import Any, Dict, List

from ai_api_client_sdk.models.metric import Metric
from ai_api_client_sdk.models.metric_tag import MetricTag
from ai_api_client_sdk.models.metric_custom_info import MetricCustomInfo


class MetricResource:
    """The Metric object, defines collection of various metrics/tags/labels related to an execution.

    :param execution_id: ID of the execution
    :type execution_id: str
    :param metrics: List of the metrics related to the execution, defaults to None
    :type metrics: List[class:`ai_api_client_sdk.metric.Metric`], optional
    :param tags: List of the tags related to the execution, defaults to None
    :type tags: List[class:'ai_api_client_sdk.models.metric_tag.MetricTag'], optional
    :param custom_info: List of custom info related to the execution, defaults to None
    :type custom_info: List[class:`ai_api_client_sdk.models.metric_custom_info.MetricCustomInfo`], optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, execution_id: str, metrics: List[Metric] = None, tags: List[MetricTag] = None,
                 custom_info: List[MetricCustomInfo] = None, **kwargs):
        self.execution_id: str = execution_id
        self.metrics: List[Metric] = metrics
        self.tags: List[MetricTag] = tags
        self.custom_info: List[MetricCustomInfo] = custom_info

    def __str__(self):
        ret_string = "Metric execution id: " + str(self.execution_id) + ", Metrics: "
        for metric in self.metrics:
            ret_string += metric.name + ", "
        return ret_string[:len(ret_string) - 2]

    @staticmethod
    def from_dict(metric_resource_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.metric_resource.MetricResource` object, created from the values
        in the dict provided as parameter

        :param metric_resource_dict: Dict which includes the necessary values to create the object
        :type metric_resource_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.metric_resource.MetricResource`
        """
        if metric_resource_dict.get('metrics'):
            metric_resource_dict['metrics'] = [Metric.from_dict(m) for m in metric_resource_dict['metrics']]
        if metric_resource_dict.get('tags'):
            metric_resource_dict['tags'] = [MetricTag.from_dict(mt) for mt in metric_resource_dict['tags']]
        if metric_resource_dict.get('custom_info'):
            metric_resource_dict['custom_info'] = \
                [MetricCustomInfo.from_dict(mci) for mci in metric_resource_dict['custom_info']]
        return MetricResource(**metric_resource_dict)
