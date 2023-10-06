from typing import Dict


class DatasetCapabilities:
    """The DatasetCapabilities object represents the capabilities of the Dataset API

    :param upload: indicates whether uploading files is supported, defaults to True
    :type upload: bool, optional
    :param download: indicates whether downloading files is supported, defaults to True
    :type download: bool, optional
    :param delete: indicates whether deleting files is supported, defaults to True
    :type delete: bool, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, upload: bool = True, download: bool = True, delete: bool = True, **kwargs):
        self.upload: bool = upload
        self.download: bool = download
        self.delete: bool = delete

    @staticmethod
    def from_dict(dataset_capabilities_dict: Dict[str, bool]):
        """Returns a :class:`ai_api_client_sdk.models.dataset_capabilities.DatasetCapabilities` object, created from
        the values in the dict provided as parameter

        :param dataset_capabilities_dict: Dict which includes the necessary values to create the object
        :type dataset_capabilities_dict: Dict[str, bool]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.dataset_capabilities.DatasetCapabilities`
        """
        return DatasetCapabilities(**dataset_capabilities_dict)

    def __eq__(self, other):
        if not isinstance(other, DatasetCapabilities):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
