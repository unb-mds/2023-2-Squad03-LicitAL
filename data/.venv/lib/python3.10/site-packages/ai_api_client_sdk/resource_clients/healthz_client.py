from ai_api_client_sdk.models.healthz_status import HealthzStatus
from ai_api_client_sdk.resource_clients.base_client import BaseClient


class HealthzClient(BaseClient):
    """HealthzClient is a class implemented for interacting with the healthz endpoint of the server. It implements the
    base class :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """

    def get(self) -> HealthzStatus:
        """Retrieves the health status of the server.

        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: The health status of the server
        :rtype: class:`ai_api_client_sdk.models.healthz_status.HealthzStatus`
        """
        healthz_status_dict = self.rest_client.get(path='/healthz')
        return HealthzStatus.from_dict(healthz_status_dict)
