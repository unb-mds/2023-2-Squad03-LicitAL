from typing import Any, Dict

from ai_api_client_sdk.models.extensions_analytics import ExtensionsAnalytics
from ai_api_client_sdk.models.extensions_dataset import ExtensionsDataset
from ai_api_client_sdk.models.extensions_resource_groups import ExtensionsResourceGroups


class Extensions:
    """The Extensions object represents the extensions to the AI API

    :param analytics: Metadata and capabilities of the Analytics API, defaults to None
    :type analytics: class:`ai_api_client_sdk.models.extensions_analytics.ExtensionsAnalytics`, optional
    :param resource_groups: Metadata and capabilities of the Resource Groups API, defaults to None
    :type resource_groups: class:`ai_api_client_sdk.models.extensions_resource_groups.ExtensionsResourceGroups`,
        optional
    :param dataset: Metadata and capabilities of the Dataset API, defaults to None
    :type dataset: class:`ai_api_client_sdk.models.extensions_dataset.ExtensionsDataset`, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, analytics: ExtensionsAnalytics = None, resource_groups: ExtensionsResourceGroups = None,
                 dataset: ExtensionsDataset = None, **kwargs):
        self.analytics: ExtensionsAnalytics = analytics
        self.resource_groups: ExtensionsResourceGroups = resource_groups
        self.dataset: ExtensionsDataset = dataset

    @staticmethod
    def from_dict(extensions_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.extensions.Extensions` object, created from the values in the
        dict provided as parameter

        :param extensions_dict: Dict which includes the necessary values to create the object
        :type extensions_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.extensions.Extensions`
        """
        if 'analytics' in extensions_dict:
            extensions_dict['analytics'] = ExtensionsAnalytics.from_dict(extensions_dict['analytics'])
        if 'resource_groups' in extensions_dict:
            extensions_dict['resource_groups'] = ExtensionsResourceGroups.from_dict(extensions_dict['resource_groups'])
        if 'dataset' in extensions_dict:
            extensions_dict['dataset'] = ExtensionsDataset.from_dict(extensions_dict['dataset'])
        return Extensions(**extensions_dict)

    def __eq__(self, other):
        if not isinstance(other, Extensions):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
