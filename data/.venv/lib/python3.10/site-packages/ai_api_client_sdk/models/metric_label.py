from typing import Dict

from .base_models import NameValue


class MetricLabel(NameValue):
    """The MetricLabel object defines a metric label as a name-value pair. Refer to
    :class:`ai_api_client_sdk.models.base_models.NameValue`, for the object definition
    """
    @staticmethod
    def from_dict(metric_label_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.metric_label.MetricLabel` object, created from the values in the
        dict provided as parameter

        :param metric_label_dict: Dict which includes the necessary values to create the object
        :type metric_label_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.metric_label.MetricLabel`
        """
        return MetricLabel(**metric_label_dict)

    def to_dict(self):
        """Returns the attributes of the object as a dictionary

        :return: A dict, including all the attributes of the object
        :rtype: Dict[str, str]
        """
        return {'name': self.name, 'value': self.value}
