from typing import Any, Dict

from .base_models import BasicResponse
from .status import Status


class DeploymentCreateResponse(BasicResponse):
    """The DeploymentCreateResponse object defines the response of the deployment create query
    :param id: ID of the deployment
    :type id: str
    :param message: Response message from the server
    :type message: str
    :param deployment_url: URL of the running deployment
    :type deployment_url: str
    :param status: Status of the deployment
    :type status: class:`ai_api_client_sdk.models.status.Status`
    :param ttl: Time to live for deployment
    :type ttl: str, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, message: str, deployment_url: str, status: Status, ttl: str = None, **kwargs):
        super().__init__(id=id, message=message, **kwargs)
        self.deployment_url: str = deployment_url
        self.status: Status = status
        self.ttl: str = ttl

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.deployment_create_response.DeploymentCreateResponse` object,
        created from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.deployment_create_response.DeploymentCreateResponse`
        """
        response_dict['status'] = Status(response_dict['status'])
        return DeploymentCreateResponse(**response_dict)
