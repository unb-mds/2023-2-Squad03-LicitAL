from typing import List, Union, Dict
from .base_models import BasicResponse, BulkModifyErrorResponse


class DeploymentBulkModifyResponse:
    """The DeploymentBulkModifyResponse object defines the response to the deployments bulk modify request
    :param deployments: Response to the bulk modify request of deployments
    :type deployments: List[Union[BasicResponse, BulkModifyErrorResponse]]
    """
    def __init__(self, deployments: List[Union[BasicResponse, BulkModifyErrorResponse]], **kwargs):
        self.deployments: List[Union[BasicResponse, BulkModifyErrorResponse]] = deployments
      
    def __str__(self):
        dbmr_str = ''
        for d in self.deployments:
            dbmr_str += f'{d.__str__()}\n'
        return dbmr_str

    @staticmethod
    def from_dict(response_dict: Dict[str, List[Dict[str, Union[str, Dict]]]]):
        """Returns a :class:`ai_api_client_sdk.models.Deployment_Bulk_Modify_Response.DeploymentBulkModifyResponse`
        object, created from the values provided as parameter

        :param response_dict: Which includes the necessary values to create the object
        :type response_dict: Dict[str, List[Dict[str, Union[str, Dict]]]]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.Deployment_Bulk_Modify_Response.DeploymentBulkModifyResponse`
        """
        response_dict['deployments'] = [
            BulkModifyErrorResponse.from_dict(d) if 'error' in d else BasicResponse.from_dict(d)
            for d in response_dict['deployments']
        ]

        return DeploymentBulkModifyResponse(**response_dict)
