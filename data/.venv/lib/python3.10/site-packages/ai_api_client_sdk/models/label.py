from typing import Dict

from .base_models import KeyValue


class Label(KeyValue):
    """The Label object defines a label as a key-value pair. Refer to
    :class:`ai_api_client_sdk.models.base_models.KeyValue`, for the object definition
    """

    def __str__(self):
        return "Label key: " + str(self.key) + ", Label value: " + str(self.value)

    @staticmethod
    def from_dict(label_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.label.Label` object, created from the values in the dict provided
        as parameter

        :param label_dict: Dict which includes the necessary values to create the object
        :type label_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.label.Label`
        """
        return Label(**label_dict)
