from datetime import datetime
from typing import Any, Dict

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime


class Version:
    """The Version object defines a scenario
    :param id: ID of the version
    :type id: str
    :param scenario_id: ID of the scenario the version belongs to
    :type scenario_id: str
    :param created_at: Time when the scenario was created
    :type created_at: datetime
    :param modified_at: Time when the scenario was last modified
    :type modified_at: datetime
    :param description: Description of the scenario, defaults to None
    :type description: str, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, scenario_id: str, created_at: datetime, modified_at: datetime, description: str = None,
                 **kwargs):
        self.id: str = id
        self.scenario_id: str = scenario_id
        self.description: str = description
        self.created_at: datetime = created_at
        self.modified_at: datetime = modified_at

    def __str__(self):
        return "Version id: " + str(self.id)

    @staticmethod
    def from_dict(version_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.version.Version` object, created from the values in the dict
        provided as parameter

        :param version_dict: Dict which includes the necessary values to create the object
        :type version_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.version.Version`
        """
        version_dict['created_at'] = parse_datetime(version_dict['created_at'])
        version_dict['modified_at'] = parse_datetime(version_dict['modified_at'])
        return Version(**version_dict)
