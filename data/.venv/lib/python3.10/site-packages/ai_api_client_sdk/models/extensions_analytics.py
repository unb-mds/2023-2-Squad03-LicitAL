from typing import Dict


class ExtensionsAnalytics:
    """The ExtensionsAnalytics object represents the metadata and capabilities of the Analytics API

    :param version: Version of the Analytics API
    :type version: str
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, version: str, **kwargs):
        self.version: str = version

    @staticmethod
    def from_dict(extensions_analytics_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.extensions_analytics.ExtensionsAnalytics` object, created from
        the values in the dict provided as parameter

        :param extensions_analytics_dict: Dict which includes the necessary values to create the object
        :type extensions_analytics_dict: Dict[str, str]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.extensions_analytics.ExtensionsAnalytics`
        """
        return ExtensionsAnalytics(**extensions_analytics_dict)

    def __eq__(self, other):
        if not isinstance(other, ExtensionsAnalytics):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
