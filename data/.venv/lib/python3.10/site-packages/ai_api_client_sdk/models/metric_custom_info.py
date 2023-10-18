from typing import Dict

from .base_models import NameValue


class MetricCustomInfo(NameValue):
    """The MetricCustomInfo object defines rendering/semantic information regarding certain metric for consuming
    application or complex metrics in JSON format, as a name-value pair. Refer to
    :class:`ai_api_client_sdk.models.base_models.NameValue`, for the object definition
    """
    @staticmethod
    def from_dict(metric_custom_info_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.metric_custom_info.MetricCustomInfo` object, created from the
        values in the dict provided as parameter

        :param metric_custom_info_dict: Dict which includes the necessary values to create the object
        :type metric_custom_info_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.metric_custom_info.MetricCustomInfo`
        """
        return MetricCustomInfo(**metric_custom_info_dict)
