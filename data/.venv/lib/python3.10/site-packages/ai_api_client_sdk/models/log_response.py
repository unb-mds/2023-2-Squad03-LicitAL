from datetime import datetime
from typing import Any, Dict, List

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime


class LogResultItem:
    """The LogResultItem object defines each item in the log response
    :param msg: log message
    :type msg: str
    :param timestamp: timestamp corresponding to the log message
    :type timestamp: datetime
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, msg: str, timestamp: datetime, **kwargs):
        self.msg: str = msg
        self.timestamp: datetime = timestamp

    @staticmethod
    def from_dict(log_result_item_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.log_response.LogResultItem` object, created from the values
        in the dict provided as parameter

        :param log_result_item_dict: Dict which includes the necessary values to create the object
        :type log_result_item_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.log_response.LogResultItem`
        """
        log_result_item_dict['timestamp'] = parse_datetime(log_result_item_dict['timestamp'])
        return LogResultItem(**log_result_item_dict)


class LogResponseData:
    """The LogResponseData object defines the data of the log response
    :param result: result of the log query
    :type result: List[class:`ai_api_client_sdk.models.log_response.LogResponseResultItem`]
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, result: List[LogResultItem], **kwargs):
        self.result: List[LogResultItem] = result

    @staticmethod
    def from_dict(log_response_data_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.log_response.LogResponseData` object, created from the values
        in the dict provided as parameter

        :param log_response_data_dict: Dict which includes the necessary values to create the object
        :type log_response_data_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.log_response.LogResponseData`
        """
        log_response_data_dict['result'] = [LogResultItem.from_dict(r) for r in log_response_data_dict['result']]
        return LogResponseData(**log_response_data_dict)


class LogResponse:
    """The LogResponse object defines the response of the log request
    :param data: log response data
    :type data: class:`ai_api_client_sdk.models.log_response.LogResponseData`
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, data: LogResponseData, **kwargs):
        self.data: LogResponseData = data

    def __str__(self):
        res_str = "Log response messages: "
        for result_item in self.data.result:
            res_str += str(result_item.msg) + ", "
        return res_str[:len(res_str) - 2]

    @staticmethod
    def from_dict(log_response_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.log_response.LogResponse` object, created from the values
        in the dict provided as parameter

        :param log_response_dict: Dict which includes the necessary values to create the object
        :type log_response_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.log_response.LogResponse`
        """
        log_response_dict['data'] = LogResponseData.from_dict(log_response_dict['data'])
        return LogResponse(**log_response_dict)
