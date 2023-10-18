from typing import Any, Dict

from ai_api_client_sdk.models.ai_api_capabilities import AIAPICapabilities
from ai_api_client_sdk.models.ai_api_limits import AIAPILimits


class AIAPIMeta:
    """The AIAPIMeta object represents the metadata and capabilities of the AI API

    :param version: version of the AI API
    :type version: str
    :param capabilities: capabilities of AI API, defaults to None
    :type capabilities: class:`ai_api_client_sdk.models.ai_api_capabilities.AIAPICapabilities`
    :param limits: limits of AI API, defaults to None
    :type limits: class:`ai_api_client_sdk.models.ai_api_limits.AIAPILimits`, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, version: str, capabilities: AIAPICapabilities = None, limits: AIAPILimits = None, **kwargs):
        self.version: str = version
        self.capabilities: AIAPICapabilities = capabilities
        self.limits: AIAPILimits = limits

    @staticmethod
    def from_dict(ai_api_meta_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.ai_api_meta.AIAPIMeta` object, created
        from the values in the dict provided as parameter

        :param ai_api_meta_dict: Dict which includes the necessary values to create the object
        :type ai_api_meta_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.ai_api_meta.AIAPIMeta`
        """
        if 'capabilities' in ai_api_meta_dict:
            ai_api_meta_dict['capabilities'] = AIAPICapabilities.from_dict(ai_api_meta_dict['capabilities'])
        if 'limits' in ai_api_meta_dict:
            ai_api_meta_dict['limits'] = AIAPILimits.from_dict(ai_api_meta_dict['limits'])
        return AIAPIMeta(**ai_api_meta_dict)

    def __eq__(self, other):
        if not isinstance(other, AIAPIMeta):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
