from typing import Dict, Any

from ai_api_client_sdk.models.ai_api_limits_deployments import AIAPILimitsDeployments
from ai_api_client_sdk.models.ai_api_limits_executions import AIAPILimitsExecutions


class AIAPILimits:
    """The AIAPILimits object represents the the limits for executions and deployments

    :param executions: represents the limits for executions, defaults to None
    :type executions: class:`ai_api_client_sdk.models.ai_api_limits_executions.AIAPILimitsExecutions`, optional
    :param deployments: represents the limits for deployments, defaults to None
    :type deployments: class:`ai_api_client_sdk.models.ai_api_limits_deployments.AIAPILimitsDeployments`, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, executions: AIAPILimitsExecutions = None, deployments: AIAPILimitsDeployments = None, **kwargs):
        self.executions: AIAPILimitsExecutions = executions
        self.deployments: AIAPILimitsDeployments = deployments

    @staticmethod
    def from_dict(ai_api_limits_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.ai_api_limits.AIAPILimits` object, created from the values in the
        dict provided as parameter

        :param ai_api_limits_dict: Dict which includes the necessary values to create the object
        :type ai_api_limits_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.ai_api_limits.AIAPILimits`
        """
        if 'executions' in ai_api_limits_dict:
            ai_api_limits_dict['executions'] = AIAPILimitsExecutions.from_dict(ai_api_limits_dict['executions'])
        if 'deployments' in ai_api_limits_dict:
            ai_api_limits_dict['deployments'] = AIAPILimitsDeployments.from_dict(ai_api_limits_dict['deployments'])
        return AIAPILimits(**ai_api_limits_dict)

    def __eq__(self, other):
        if not isinstance(other, AIAPILimits):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
