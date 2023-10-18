from typing import Any, Dict, List

from ai_core_sdk.models import QueryResponse
from ai_core_sdk.models.resource_group import ResourceGroup


class ResourceGroupQueryResponse(QueryResponse):
    """The ResourceGroupQueryResponse object defines the response of the resourceGroups query request
    :param resources: List of the resource groups returned from the server
    :type resources: List[class:`ai_core_sdk.models.resource_group.ResourceGroup`]
    :param count: Total number of the queried docker registry secrets
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """

    def __init__(self, resources: List[ResourceGroup], count: int, **kwargs):
        super().__init__(resources=resources, count=count, **kwargs)

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a
        :class:`ai_core_sdk.models.docker_registry_secret_query_response.DockerRegistrySecretQueryResponse`
        object, created from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.docker_registry_secret_query_response.DockerRegistrySecretQueryResponse`
        """
        response_dict['resources'] = [ResourceGroup.from_dict(r) for r in response_dict['resources']]
        return ResourceGroupQueryResponse(**response_dict)
