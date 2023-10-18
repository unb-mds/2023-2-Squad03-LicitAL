from typing import Any, Dict, List

from ai_core_sdk.models import QueryResponse
from ai_core_sdk.models.repository import Repository


class RepositoryQueryResponse(QueryResponse):
    """The RepositoryQueryResponse object defines the response of the repository query request
    :param resources: List of the repositories returned from the server
    :type resources: List[class:`ai_core_sdk.models.repository.Repository`]
    :param count: Total number of the queried repositories
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, resources: List[Repository], count: int, **kwargs):
        super().__init__(resources=resources, count=count, **kwargs)

    @staticmethod
    def from_dict(response_dict: Dict[str, Any]):
        """Returns a
        :class:`ai_core_client_sdk.models.repository_query_response.RepositoryQueryResponse`
        object, created from the values in the dict provided as parameter

        :param response_dict: Dict which includes the necessary values to create the object
        :type response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.repository_query_response.RepositoryQueryResponse`
        """
        response_dict['resources'] = [Repository.from_dict(r) for r in response_dict['resources']]
        return RepositoryQueryResponse(**response_dict)
