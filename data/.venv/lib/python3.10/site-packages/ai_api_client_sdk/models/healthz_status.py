from enum import Enum
from typing import Any, Dict


class HealthStatus(Enum):
    READY = 'READY'
    NOT_READY = 'NOT READY'


class HealthzStatus:
    """The HealthzStatus object defines the response of the healthz endpoint
    :param status: Health status of the server
    :type status: class:`ai_api_client_sdk.models.healthz_status.HealthStatus`
    :param message: Response message from the server
    :type message: str
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, status: HealthStatus, message: str, **kwargs):
        self.status: HealthStatus = status
        self.message: str = message

    def __str__(self):
        return "Healthz status message: " + str(self.message)

    @staticmethod
    def from_dict(healthz_status_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.healthz_status.HealthzStatus` object, created from the values in
        the dict provided as parameter

        :param healthz_status_dict: Dict which includes the necessary values to create the object
        :type healthz_status_dict: Dict[str, str]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.healthz_status.HealthzStatus`
        """
        healthz_status_dict['status'] = HealthStatus(healthz_status_dict['status'])
        return HealthzStatus(**healthz_status_dict)
