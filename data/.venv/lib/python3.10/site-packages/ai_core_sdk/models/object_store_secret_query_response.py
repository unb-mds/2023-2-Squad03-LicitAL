from typing import Any, Dict, List

from ai_core_sdk.models import QueryResponse
from ai_core_sdk.models.object_store_secret import ObjectStoreSecret


class ObjectStoreSecretQueryResponse(QueryResponse):
    """The ObjectStoreSecretQueryResponse object defines the response of the object store secret query request
    :param resources: List of the object store secrets returned from the server
    :type resources: List[class:`ai_core_sdk.models.object_store_secret.ObjectStoreSecret`]
    :param count: Total number of the queried object store secrets
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, resources: List[ObjectStoreSecret], count: int, **kwargs):
        super().__init__(resources=resources, count=count, **kwargs)

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a
        :class:`ai_core_sdk.models.object_store_secret_query_response.ObjectStoreSecretQueryResponse`
        object, created from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.object_store_secret_query_response.ObjectStoreSecretQueryResponse`
        """
        response_dict['resources'] = [ObjectStoreSecret.from_dict(r) for r in response_dict['resources']]
        return ObjectStoreSecretQueryResponse(**response_dict)
