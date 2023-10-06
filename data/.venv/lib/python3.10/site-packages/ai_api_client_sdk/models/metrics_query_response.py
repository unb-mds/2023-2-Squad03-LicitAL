from typing import Any, Dict, List

from .base_models import QueryResponse
from .metric_resource import MetricResource


class MetricsQueryResponse(QueryResponse):
    """The MetricsQueryResponse object defines the response of the metrics query request
    :param resources: List of the metrics returned from the server
    :type resources: List[class:`ai_api_client_sdk.models.metrics_resource.MetricResource`]
    :param count: Total number of the queried metrics
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, resources: List[MetricResource], count: int, **kwargs):
        super().__init__(resources=resources, count=count, **kwargs)

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.metrics_query_response.MetricsQueryResponse` object, created
        from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.metrics_query_response.MetricsQueryResponse`
        """
        response_dict['resources'] = [MetricResource.from_dict(r) for r in response_dict['resources']]
        return MetricsQueryResponse(**response_dict)
