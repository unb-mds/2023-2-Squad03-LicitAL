import os
from typing import Dict
from xmlrpc.client import Boolean

from ai_api_client_sdk.helpers.authenticator import Authenticator


def form_top_skip_params(top: int = None, skip: int = None) -> Dict[str, int]:
    """
    Frame query param

    :param top: Number of objects to be retrieved, defaults to None
    :type top: int, optional
    :param skip: Number of objects to be skipped, from the list of the queried objects,
        defaults to None
    :type skip: int, optional
    """
    params = {}
    if top:
        params['$top'] = top
    if skip:
        params['$skip'] = skip
    if not params:
        params = None
    return params


def is_within_aicore() -> Boolean:
    """[summary]
    Function to check whether the sdk is used within or out of aicore cluster
    Returns:
        Boolean: True if the ai-core-sdk is used within aicore cluster
                 False if the ai-core-sdk is used outside aicore cluster
    """
    return os.getenv('AICORE_EXECUTION_ID') and os.getenv('AICORE_TRACKING_ENDPOINT')
