from typing import Dict


class DatasetLimits:
    """The DatasetLimits object represents the limits of the Dataset API

    :param max_upload_file_size: Max size (in bytes) of a single uploaded file, defaults to 104857600
    :type max_upload_file_size: int, optional
    :param max_files_per_dataset: Max number of files per dataset. <0 means unlimited, defaults to -1
    :type max_files_per_dataset: int, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, max_upload_file_size: int = 104857600, max_files_per_dataset: int = -1, **kwargs):
        self.max_upload_file_size: int = max_upload_file_size
        self.max_files_per_dataset: int = max_files_per_dataset

    @staticmethod
    def from_dict(dataset_limits_dict: Dict[str, int]):
        """Returns a :class:`ai_api_client_sdk.models.dataset_limits.DatasetLimits` object, created from the values in
        the dict provided as parameter

        :param dataset_limits_dict: Dict which includes the necessary values to create the object
        :type dataset_limits_dict: Dict[str, int]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.dataset_limits.DatasetLimits`
        """
        return DatasetLimits(**dataset_limits_dict)

    def __eq__(self, other):
        if not isinstance(other, DatasetLimits):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
