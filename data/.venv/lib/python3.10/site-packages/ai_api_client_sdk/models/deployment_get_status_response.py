from datetime import datetime
from typing import Any, Dict

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime
from ai_api_client_sdk.models.enactment_get_status_response import EnactmentGetStatusResponse
from ai_api_client_sdk.models.status import Status


class DeploymentGetStatusResponse(EnactmentGetStatusResponse):
    """The DeploymentGetStatusResponse object defines the response of the deployment get status
    :param id: ID of the deployment
    :type id: str
    :param configuration_id: ID of the configuration which configured the deployment
    :type configuration_id: str
    :param status: Status of the deployment
    :type status: class:`ai_api_client_sdk.models.status.Status`
    :param created_at: Time when the deployment was created
    :type created_at: datetime
    :param modified_at: Time when the deployment was last modified
    :type modified_at: datetime
    :param status_details: A dict, which gives detailed information about the status of the deployment, defaults to None
    :type status_details: Dict[str, Any], optional
    """
    def __init__(self, id: str, configuration_id: str,
                 status: Status, created_at: datetime, modified_at: datetime, status_details: Dict[str, Any] = None):
        super().__init__(id=id, configuration_id=configuration_id, status=status, created_at=created_at,
                         modified_at=modified_at, status_details=status_details)

    def __str__(self):
        return "Deployment id: " + str(self.id)

    @staticmethod
    def from_dict(deployment_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.deployment_get_status_response.DeploymentGetStatusResponse`
        object, created from the values in the dict provided as parameter
        :param deployment_dict: Dict which includes the necessary values to create the object
        :type deployment_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.deployment_get_status_response.DeploymentGetStatusResponse`
        """
        deployment_dict['status'] = Status(deployment_dict['status'])
        deployment_dict['created_at'] = parse_datetime(deployment_dict['created_at'])
        deployment_dict['modified_at'] = parse_datetime(deployment_dict['modified_at'])
        return DeploymentGetStatusResponse(**deployment_dict)
