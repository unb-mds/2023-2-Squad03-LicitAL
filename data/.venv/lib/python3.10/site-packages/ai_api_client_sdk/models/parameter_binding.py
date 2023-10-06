from typing import Dict

from .base_models import KeyValue


class ParameterBinding(KeyValue):
    """The ParameterBinding object defines the input artifact specified in the configuration, as a key-value pair. Refer
    to :class:`ai_api_client_sdk.models.base_models.KeyValue`, for the object definition
    """

    def __str__(self):
        return "Parameter binding key: " + str(self.key) + "Parameter binding value: " + str(self.value)

    @staticmethod
    def from_dict(parameter_binding_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.parameter_binding.ParameterBinding` object, created from
        the values in the dict provided as parameter

        :param parameter_binding_dict: Dict which includes the necessary values to create the object
        :type parameter_binding_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.parameter_binding.ParameterBinding`
        """
        return ParameterBinding(**parameter_binding_dict)
