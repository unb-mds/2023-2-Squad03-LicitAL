from typing import Any, Dict

from ai_api_client_sdk.models.dataset_capabilities import DatasetCapabilities
from ai_api_client_sdk.models.dataset_limits import DatasetLimits


class ExtensionsDataset:
    """The ExtensionsDataset object represents the metadata and capabilities of the Dataset API

    :param version: Version of the Dataset API
    :type version: str
    :param capabilities: Capabilities of the Dataset API, defaults to None
    :type capabilities: class:`ai_api_client_sdk.models.dataset_capabilities.DatasetCapabilities`, optional
    :param limits: Limits of the Dataset API, defaults to None
    :type limits: class:`ai_api_client_sdk.models.dataset_limits.DatasetLimits`, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, version: str, capabilities: DatasetCapabilities = None, limits: DatasetLimits = None, **kwargs):
        self.version: str = version
        self.capabilities: DatasetCapabilities = capabilities
        self.limits: DatasetLimits = limits

    @staticmethod
    def from_dict(extensions_dataset_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.extensions_dataset.ExtensionsDataset` object, created from the
        values in the dict provided as parameter

        :param extensions_dataset_dict: Dict which includes the necessary values to create the object
        :type extensions_dataset_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.extensions_dataset.ExtensionsDataset`
        """
        if 'capabilities' in extensions_dataset_dict:
            extensions_dataset_dict['capabilities'] = \
                DatasetCapabilities.from_dict(extensions_dataset_dict['capabilities'])
        if 'limits' in extensions_dataset_dict:
            extensions_dataset_dict['limits'] = DatasetLimits.from_dict(extensions_dataset_dict['limits'])
        return ExtensionsDataset(**extensions_dataset_dict)

    def __eq__(self, other):
        if not isinstance(other, ExtensionsDataset):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
