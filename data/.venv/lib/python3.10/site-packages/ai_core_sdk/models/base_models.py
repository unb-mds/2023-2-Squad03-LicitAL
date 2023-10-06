from typing import Dict


class BasicNameResponse:
    """The BasicNameResponse object defines the response with name from the server

    :param name: Name of the relevant resource
    :type id: str
    :param message: Response message from the server
    :type message: str
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """

    def __init__(self, name: str, message: str, **kwargs):
        self.name: str = name
        self.message: str = message

    def __str__(self):
        return "Name: " + str(self.name) + ", Message: " + str(self.message)

    @staticmethod
    def from_dict(bnr_dict: Dict[str, str]):
        """Returns a :class:`ai_core_sdk.models.base_models.BasicNameResponse` object, created from the values in the
        dict provided as parameter

        :param bnr_dict: Dict which includes the necessary values to create the object
        :type bnr_dict: Dict[str, str]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.base_models.BasicNameResponse`
        """
        return BasicNameResponse(**bnr_dict)


class Message:
    """Message object defines a message

    :param message: message
    :type message: str
    """

    def __init__(self, message: str, **kwargs):
        self.message: str = message

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False
        return self.message == other.message

    def __str__(self):
        return "Message: " + str(self.message)

    @staticmethod
    def from_dict(message_dict: Dict[str, str]):
        """Returns a :class:`ai_core_sdk.models.base_models.Message` object, created from the values in the
        dict provided as parameter

        :param message_dict: Dict which includes the necessary values to create the object
        :type message_dict: Dict[str, str]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.base_models.Message`
        """
        return Message(**message_dict)
