from typing import Dict

from .base_models import NameValue


class MetricTag(NameValue):
    """The MetricTag object defines a tag as a name-value pair. Refer to
    :class:`ai_api_client_sdk.models.base_models.NameValue`, for the object definition
    """

    def __str__(self):
        return "Metric tag name: " + str(self.name) + "Metric tag value: " + str(self.value)

    @staticmethod
    def from_dict(metric_tag_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.metric_tag.MetricTag` object, created from the values in the dict
        provided as parameter

        :param metric_tag_dict: Dict which includes the necessary values to create the object
        :type metric_tag_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.metric_tag.MetricTag`
        """
        return MetricTag(**metric_tag_dict)
