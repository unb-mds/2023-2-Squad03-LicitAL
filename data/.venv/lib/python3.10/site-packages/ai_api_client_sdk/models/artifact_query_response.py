from typing import Any, Dict, List

from .artifact import Artifact
from .base_models import QueryResponse


class ArtifactQueryResponse(QueryResponse):
    """The ArtifactQueryResponse object defines the response of the artifact query request
    :param resources: List of the artifacts returned from the server
    :type resources: List[class:`ai_api_client_sdk.models.artifact.Artifact`]
    :param count: Total number of the queried artifacts
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, resources: List[Artifact], count: int, **kwargs):
        super().__init__(resources=resources, count=count, **kwargs)

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.artifact_query_response.ArtifactQueryResponse` object, created
        from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.artifact_query_response.ArtifactQueryResponse`
        """
        response_dict['resources'] = [Artifact.from_dict(r) for r in response_dict['resources']]
        return ArtifactQueryResponse(**response_dict)
