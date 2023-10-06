from datetime import datetime
from enum import Enum
from typing import Any, Dict

from ai_api_client_sdk.helpers.datetime_parser import DATETIME_FORMAT
from ai_api_client_sdk.helpers.rest_client import RestClient


class BaseClient:
    """BaseClient defines the interface for the resource clients.

    :param rest_client: the client used to make calls to the server
    :type rest_client: class:`ai_api_client_sdk.helpers.rest_client.RestClient`
    """

    def __init__(self, rest_client: RestClient):
        self.rest_client: RestClient = rest_client

    def create(self, *args, **kwargs):
        """Creates the relevant resource. Will be implemented by the respective resource clients"""
        raise NotImplementedError()

    def delete(self, *args, **kwargs):
        """Deletes the relevant resource. Will be implemented by the respective resource clients"""
        raise NotImplementedError()

    def get(self, *args, **kwargs):
        """Retrieves the relevant resource. Will be implemented by the respective resource clients"""
        raise NotImplementedError()

    def modify(self, *args, **kwargs):
        """Modifies the relevant resource. Will be implemented by the respective resource clients"""
        raise NotImplementedError()

    def bulk_modify(self, *args, **kwargs):
        """Modifies multiple instances of the relevant resource. Will be implemented by the respective resource clients"""
        raise NotImplementedError()

    def query(self, *args, **kwargs):
        """Queries the relevant resources. Will be implemented by the respective resource clients"""
        raise NotImplementedError()

    def count(self, *args, **kwargs):
        """Counts the relevant resources. Will be implemented by the respective resource clients"""
        raise NotImplementedError()

    def query_logs(self, *args, **kwargs):
        """Queries the relevant logs. Will be implemented by the respective resource clients"""
        raise NotImplementedError()

    @staticmethod
    def _form_query_params(**kwargs) -> Dict[str, Any]:
        """Creates a params dict, from the keyword arguments. Reforms the list parameters into the expected form by the
        server

        :param kwargs: keyword arguments which are to be reformed to a dict.
        :return: A dict, defining the parameters
        :rtype: Dict[str, Any]
        """
        params = {}
        for k, v in kwargs.items():
            if v:
                if isinstance(v, list):
                    v = ','.join(v)
                elif isinstance(v, datetime):
                    v = v.strftime(DATETIME_FORMAT)
                elif isinstance(v, Enum):
                    v = v.value
                params[k] = v
        if 'search' in params:
            params['$search'] = params['search']
            del params['search']
        if 'expand' in params:
            params['$expand'] = params['expand']
            del params['expand']
        if 'select' in params:
            params['$select'] = params['select']
            del params['select']
        return params if len(params) > 0 else None
