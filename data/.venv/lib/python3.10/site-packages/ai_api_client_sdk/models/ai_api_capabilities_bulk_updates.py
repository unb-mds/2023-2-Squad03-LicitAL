from typing import Dict


class AIAPICapabilitiesBulkUpdates:
    """The AIAPICapabilitiesBulkUpdates object represents the bulk updates capabilities

    :param deployments: indicates whether bulk updates for executions are supported, defaults to False
    :type deployments: bool, optional
    :param executions: indicates whether bulk updates for executions are supported, defaults to False
    :type executions: bool, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, executions: bool = False, deployments: bool = False, **kwargs):
        self.executions: bool = executions
        self.deployments: bool = deployments

    @staticmethod
    def from_dict(ai_api_capabilities_bulk_updates_dict: Dict[str, bool]):
        """Returns a :class:`ai_api_client_sdk.models.ai_api_capabilities_bulk_updates.AIAPICapabilitiesBulkUpdates` object, created
        from the values in the dict provided as parameter

        :param ai_api_capabilities_bulk_updates_dict: Dict which includes the necessary values to create the object
        :type ai_api_capabilities_bulk_updates_dict: Dict[str, bool]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.ai_api_capabilities_bulk_updates.AIAPICapabilitiesBulkUpdates`
        """
        return AIAPICapabilitiesBulkUpdates(**ai_api_capabilities_bulk_updates_dict)

    def __eq__(self, other):
        if not isinstance(other, AIAPICapabilitiesBulkUpdates):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
