from typing import Any, Dict

from .base_models import BasicResponse


class ArtifactCreateResponse(BasicResponse):
    """The ArtifactCreateResponse object defines the response of the artifact create request
    :param id: ID of the artifact
    :type id: str
    :param message: Response message from the server
    :type message: str
    :param url: URL of the artifact
    :type url: str
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, message: str, url: str, **kwargs):
        super().__init__(id=id, message=message, **kwargs)
        self.url: str = url

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.artifact_create_response.ArtifactCreateResponse` object, created
        from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.artifact_create_response.ArtifactCreateResponse`
        """
        return ArtifactCreateResponse(**response_dict)
