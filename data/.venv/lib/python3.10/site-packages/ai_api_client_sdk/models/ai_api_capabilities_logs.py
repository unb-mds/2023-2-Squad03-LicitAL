from typing import Dict


class AIAPICapabilitiesLogs:
    """The AIAPICapabilitiesLogs object represents the log capabilities

    :param user_executions: indicates whether logs for executions are supported, defaults to True
    :type user_executions: bool, optional
    :param user_deployments: indicates whether logs for deployments are supported, defaults to True
    :type user_deployments: bool, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, executions: bool = True, deployments: bool = True, **kwargs):
        self.executions: bool = executions
        self.deployments: bool = deployments

    @staticmethod
    def from_dict(ai_api_capabilities_logs_dict: Dict[str, bool]):
        """Returns a :class:`ai_api_client_sdk.models.ai_api_capabilities_logs.AIAPICapabilitiesLogs` object, created
        from the values in the dict provided as parameter

        :param ai_api_capabilities_logs_dict: Dict which includes the necessary values to create the object
        :type ai_api_capabilities_logs_dict: Dict[str, bool]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.ai_api_capabilities_logs.AIAPICapabilitiesLogs`
        """
        return AIAPICapabilitiesLogs(**ai_api_capabilities_logs_dict)

    def __eq__(self, other):
        if not isinstance(other, AIAPICapabilitiesLogs):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
