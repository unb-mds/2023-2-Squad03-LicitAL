from typing import Dict, List

from ai_api_client_sdk.models.api_version import APIVersion


class VersionList:
    """The VersionList object, is a list of API version descriptions

    :param versions: A list of objects describing the API versions, defaults to None
    :type versions: class:`ai_api_client_sdk.models.api_version.APIVersion`, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, versions: List[APIVersion] = None):
        self.versions: List[APIVersion] = versions

    @staticmethod
    def from_dict(version_list_dict: Dict[str, List[Dict[str, str]]]):
        """Returns a :class:`ai_api_client_sdk.models.version_list.VersionList` object, created from the
        values in the dict provided as parameter

        :param version_list_dict: Dict which includes the necessary values to create the object
        :type version_list_dict: Dict[str, List[Dict[str, str]]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.version_list.VersionList`
        """
        if 'versions' in version_list_dict:
            for i in range(len(version_list_dict['versions'])):
                version_list_dict['versions'][i] = APIVersion.from_dict(version_list_dict['versions'][i])
        return VersionList(**version_list_dict)

    def __str__(self):
        return str(self.__dict__)
