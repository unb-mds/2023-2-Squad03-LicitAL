from enum import Enum
from typing import Dict, Union
from ai_api_client_sdk.models.target_status import TargetStatus

from aenum import Enum as AEnum


class KeyValue:
    """KeyValue object defines a key-value pair

    :param key: key of the pair
    :type key: str
    :param value: value of the pair
    :type value: str
    """

    def __init__(self, key: str, value: str, **kwargs):
        self.key: str = key
        self.value: str = value

    def to_dict(self):
        return {'key': self.key, 'value': self.value}

    def __eq__(self, other):
        if not isinstance(other, KeyValue):
            return False
        return self.key == other.key and self.value == other.value

    def __str__(self):
        return "Key: " + str(self.key) + ", Value: " + str(self.value)


class NameValue:
    """KeyValue object defines a name-value pair

    :param name: name of the pair
    :type name: str
    :param value: value of the pair
    :type value: str
    """

    def __init__(self, name: str, value: str, **kwargs):
        self.name: str = name
        self.value: str = value

    def __eq__(self, other):
        if not isinstance(other, NameValue):
            return False
        return self.name == other.name and self.value == other.value

    def __str__(self):
        return "Name: " + str(self.name) + ", Value: " + str(self.value)


class Name:
    """KeyValue object defines a name

    :param name: name
    :type name: str
    """

    def __init__(self, name: str, **kwargs):
        self.name: str = name

    def __eq__(self, other):
        if not isinstance(other, Name):
            return False
        return self.name == other.name

    def __str__(self):
        return "Name: " + str(self.name)


class QueryResponse:
    """The QueryResponse object defines the response from the server to a query request

    :param resources: List of the resources returned from the server
    :type resources: list
    :param count: Total number of the queried resources
    :type count: int
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """

    def __init__(self, resources: list, count: int, **kwargs):
        self.resources: list = resources
        self.count: int = count

    def __str__(self):
        return "Resources: [" + ", ".join(["{" + str(r) + "}" for r in self.resources]) + \
               "], Count: " + str(self.count)


class BasicResponse:
    """The BasicResponse object defines the response from the server

    :param id: ID of the relevant resource
    :type id: str
    :param message: Response message from the server
    :type message: str
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """

    def __init__(self, id: str, message: str, **kwargs):
        self.id: str = id
        self.message: str = message

    def __str__(self):
        return "Id: " + str(self.id) + ", Message: " + str(self.message)

    @staticmethod
    def from_dict(br_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.base_models.BasicResponse` object, created from the values in the
        dict provided as parameter

        :param br_dict: Dict which includes the necessary values to create the object
        :type br_dict: Dict[str, str]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.base_models.BasicResponse`
        """
        return BasicResponse(**br_dict)


class BasicErrorResponse:
    """The BasicErrorResponse object defines the response from the server

    :param error_code: Error code from the server
    :type error_code: str
    :param message: Error message from the server
    :type message: str
    :param request_id: Request ID
    :type request_id: str  
    :param target: target
    :type target: str, optional
    :param details: Error details
    :type details: Dict, optional   
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """

    def __init__(self, code: str, message: str, request_id: str, target: str, details: Dict = None, **kwargs):
        self.code: str = code
        self.message: str = message
        self.request_id: str = request_id
        self.target: str = target
        self.details: Dict = details

    def __str__(self):
        return "Error code: " + str(self.code) + ", Error Message: " + str(self.message)

    @staticmethod
    def from_dict(ber_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.base_models.BasicErrorResponse` object, created from the values 
        provided as parameter

        :param ber_dict: Dict which includes the necessary values to create the object
        :type ber_dict: Dict[str, str]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.base_models.BasicErrorResponse`
        """
        return BasicErrorResponse(**ber_dict)        


class BasicModifyRequest:
    """The BasicModifyRequest object defines the request from client
    :param id: ID of the relevant resource
    :type id: str
    :param target_status: Target Status of the resource
    :type target_status: class:`ai_api_client_sdk.models.target_status.TargetStatus`
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server         
    """
    def __init__(self, id: str, target_status: TargetStatus, **kwargs):
        self.id: str = id
        self.target_status: TargetStatus = target_status

    def to_dict(self):
        return {'id': self.id, 'target_status': self.target_status.value}

    def __str__(self):
        return f'Id: {self.id}, Target Status: {self.target_status.value}'


class BulkModifyErrorResponse:
    """The BulkModifyErrorResponse object defines the error response from the server
    """
    def __init__(self, id: str, error: BasicErrorResponse, **kwargs):
        """Creates an error object for a bulk modification call

        :param id: ID of the relevant resource
        :type id: str
        :param error: Error object response from the server
        :type error: BasicErrorResponse
        :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server           
        """
        self.id = id
        self.error = error

    @staticmethod
    def from_dict(error_dict: Dict[str, Union[str, Dict]]):
        """
        :param error_dict: Dict which includes the necessary values to create the object
        :type error_dict: Dict[str, Union[str, Dict]]

        Returns:
            Returns a class:`ai_api_client_sdk.models.base_models.BulkModifyErrorResponse` object
        """
        error_dict['error'] = BasicErrorResponse.from_dict(error_dict['error'])
        return BulkModifyErrorResponse(**error_dict)

    def __str__(self):
        return f'Id: {self.id}, Error: {self.error.__str__()}'


class Order(Enum):
    ASC = 'asc'
    DESC = 'desc'


class Operation(AEnum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    CASCADE_UPDATE = 'CASCADE-UPDATE'
