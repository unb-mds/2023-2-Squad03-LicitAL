from typing import Any, Dict


class Secret:
    """The Secret object defines the secret response.

        :param name: Secret name
        :type name: str
        :param data: Secret data dictionary, defaults to None
        :type data: dict, optional
    """

    def __init__(self, name: str, data: Dict[str, str] = None, **kwargs):
        self.name: str = name
        self.data: Dict[str, str] = data

    def __str__(self):
        return "Secret name: " + str(self.name)

    @staticmethod
    def from_dict(secret_dict: Dict[str, Any]):
        """Returns a :class:`ai_core_sdk.models.secret.Secret` object, created
        from the values in the dict provided as parameter

        :param secret_dict: Dict which includes the necessary values to create the object
        :type secret_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.secret.Secret`
        """
        return Secret(**secret_dict)
