from typing import Any, Dict

from ai_api_client_sdk.models.ai_api_capabilities_bulk_updates import AIAPICapabilitiesBulkUpdates
from ai_api_client_sdk.models.ai_api_capabilities_logs import AIAPICapabilitiesLogs


class AIAPICapabilities:
    """The AIAPICapabilities object represent the capabilities of the AI API

    :param multitenant: indicates whether resource groups are supported, defaults to True
    :type multitenant: bool, optional
    :param shareable: indicates whether clients can share an instance, defaults to True
    :type shareable: bool, optional
    :param static_deployments: indicates whether the static, always running deployments are supported, defaults to True
    :type static_deployments: bool, optional
    :param user_deployments: indicates whether deployment creation by users are supported, defaults to True
    :type user_deployments: bool, optional
    :param time_to_live_deployments: indicate whether ttl value of deployment are supported, defaults to False
    :type time_to_live_deployments: bool, optional
    :param user_executions: indicates whether execution creation by users are supported, defaults to True
    :type user_executions: bool, optional
    :param bulk_updates: An object, defining the bulk updates capabilities, defaults to None
    :type bulk_updates: class:`ai_api_client_sdk.models.ai_api_capabilities_bulk_updates.AIAPICapabilitiesBulkUpdates`,
     optional
    :param execution_schedules: indicates whether execution schedules are supported, defaults to False
    :type execution_schedules: bool, optional
    :param logs: An object, defining the logs capabilities, defaults to None
    :type logs: class:`ai_api_client_sdk.models.ai_api_capabilities_logs.AIAPICapabilitiesLogs`, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """

    def __init__(self, multitenant: bool = True, shareable: bool = True, static_deployments: bool = True,
                 user_deployments: bool = True, time_to_live_deployments: bool = False, user_executions: bool = True,
                 bulk_updates: AIAPICapabilitiesBulkUpdates = None, execution_schedules: bool = False,
                 logs: AIAPICapabilitiesLogs = None, **kwargs):
        self.multitenant: bool = multitenant
        self.shareable: bool = shareable
        self.static_deployments: bool = static_deployments
        self.user_deployments: bool = user_deployments
        self.time_to_live_deployments: bool = time_to_live_deployments
        self.user_executions: bool = user_executions
        self.bulk_updates: AIAPICapabilitiesBulkUpdates = bulk_updates
        self.execution_schedules: bool = execution_schedules
        self.logs: AIAPICapabilitiesLogs = logs

    @staticmethod
    def from_dict(ai_api_capabilities_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.ai_api_capabilities.AIAPICapabilities` object, created from the
        values in the dict provided as parameter

        :param ai_api_capabilities_dict: Dict which includes the necessary values to create the object
        :type ai_api_capabilities_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.ai_api_capabilities.AIAPICapabilities`
        """
        if 'logs' in ai_api_capabilities_dict:
            ai_api_capabilities_dict['logs'] = AIAPICapabilitiesLogs.from_dict(ai_api_capabilities_dict['logs'])
        if 'bulk_updates' in ai_api_capabilities_dict:
            ai_api_capabilities_dict['bulk_updates'] = AIAPICapabilitiesBulkUpdates.from_dict(ai_api_capabilities_dict['bulk_updates'])
        return AIAPICapabilities(**ai_api_capabilities_dict)

    def __eq__(self, other):
        if not isinstance(other, AIAPICapabilities):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
