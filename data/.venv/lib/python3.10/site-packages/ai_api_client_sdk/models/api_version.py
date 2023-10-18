from typing import Dict


class APIVersion:
    """The APIVersion object represents the description of an API version

    :param version_id: API version identifier, defaults to None
    :type version_id: str, optional
    :param url: URL of the API version, defaults to None
    :type url: str, optional
    :param description: API version description
    :type description: str, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, version_id: str = None, url: str = None, description: str = None, **kwargs):
        self.version_id: str = version_id
        self.url: str = url
        self.description: str = description

    @staticmethod
    def from_dict(api_version_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.api_version.APIVersion` object, created from the
        values in the dict provided as parameter

        :param api_version_dict: Dict which includes the necessary values to create the object
        :type api_version_dict: Dict[str, str]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.api_version.APIVersion`
        """
        return APIVersion(**api_version_dict)

    def __eq__(self, other):
        if not isinstance(other, APIVersion):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return f"Version ID: {self.version_id}, URL: {self.url}"
