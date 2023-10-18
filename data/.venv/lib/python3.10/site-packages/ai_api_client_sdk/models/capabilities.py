from typing import Any, Dict

from ai_api_client_sdk.models.ai_api_meta import AIAPIMeta
from ai_api_client_sdk.models.extensions import Extensions


class Capabilities:
    """The Capabilities object represents the metadata and capabilities of, and extensions to the AI API

    :param ai_api: Metadata and capabilities of the AI API
    :type ai_api: class:`ai_api_client_sdk.models.ai_api_meta.AIAPIMeta`
    :param runtime_identifier: The name of runtime, defaults to None
    :type runtime_identifier: str, optional
    :param runtime_api_version: The version of the runtime, defaults to None
    :type runtime_api_version: str, optional
    :param description: description, defaults to None
    :type description: str, optional
    :param extensions: Extensions to the AI API, defaults to None
    :type extensions: class:`ai_api_client_sdk.models.extensions.Extensions`, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, ai_api: AIAPIMeta, runtime_identifier: str = None, runtime_api_version: str = None,
                 description: str = None, extensions: Extensions = None, **kwargs):
        self.ai_api: AIAPIMeta = ai_api
        self.runtime_identifier: str = runtime_identifier
        self.runtime_api_version: str = runtime_api_version
        self.description: str = description
        self.extensions: Extensions = extensions

    @staticmethod
    def from_dict(capabilities_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.capabilities.Capabilities` object, created
        from the values in the dict provided as parameter

        :param capabilities_dict: Dict which includes the necessary values to create the object
        :type capabilities_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.capabilities.Capabilities`
        """
        capabilities_dict['ai_api'] = AIAPIMeta.from_dict(capabilities_dict['ai_api'])
        if 'extensions' in capabilities_dict:
            capabilities_dict['extensions'] = Extensions.from_dict(capabilities_dict['extensions'])
        return Capabilities(**capabilities_dict)

    def __str__(self):
        return str(self.__dict__)
