from typing import Dict

from ai_api_client_sdk.models.ai_api_limits_enactments import AIAPILimitsEnactments


class AIAPILimitsExecutions(AIAPILimitsEnactments):
    """The AIAPILimitsExecutions object represents the the limits for executions

    :param max_running_count: max number of executions per resource group, <0 means unlimited, defaults to -1
    :type max_running_count: int, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, max_running_count: int = -1, **kwargs):
        super().__init__(max_running_count=max_running_count, **kwargs)

    @staticmethod
    def from_dict(ai_api_limits_executions_dict: Dict[str, int]):
        """Returns a :class:`ai_api_client_sdk.models.ai_api_limits_executions.AIAPILimitsExecutions` object, created
        from the values in the dict provided as parameter

        :param ai_api_limits_executions_dict: Dict which includes the necessary values to create the object
        :type ai_api_limits_executions_dict: Dict[str, int]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.ai_api_limits_executions.AIAPILimitsExecutions`
        """
        return AIAPILimitsExecutions(**ai_api_limits_executions_dict)

    def __str__(self):
        return str(self.__dict__)
