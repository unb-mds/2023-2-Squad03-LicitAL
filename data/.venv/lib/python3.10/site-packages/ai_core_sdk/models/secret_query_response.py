from typing import Any, Dict, List

from ai_core_sdk.models import QueryResponse
from ai_core_sdk.models.secret import Secret


class SecretQueryResponse(QueryResponse):
    """The SecretQueryResponse object defines the response of the secret query request
    :param resources: List of the secrets returned from the server
    :type resources: List[class:`ai_core_sdk.models.secret.Secret`]
    :param count: Total number of the queried secrets
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, resources: List[Secret], count: int, **kwargs):
        super().__init__(resources=resources, count=count, **kwargs)

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a
        :class:`ai_core_sdk.models.secret_query_response.SecretQueryResponse`
        object, created from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.secret_query_response.SecretQueryResponse`
        """
        response_dict['resources'] = [Secret.from_dict(r) for r in response_dict['resources']]
        return SecretQueryResponse(**response_dict)
