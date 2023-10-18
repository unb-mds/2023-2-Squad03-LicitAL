from datetime import datetime
from typing import Any, Dict, List

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime
from ai_api_client_sdk.models.label import Label


class Scenario:
    """The Scenario object defines a scenario
    :param id: ID of the scenario
    :type id: str
    :param created_at: Time when the scenario was created
    :type created_at: datetime
    :param modified_at: Time when the scenario was last modified
    :type modified_at: datetime
    :param name: Name of the scenario
    :type name: str
    :param description: Description of the scenario, defaults to None
    :type description: str, optional
    :param labels: List of the labels of the scenario, defaults to None
    :type labels: List[class:`ai_api_client_sdk.models.label.Label`]
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, created_at: datetime, modified_at: datetime, name: str, description: str = None,
                 labels: List[Label] = None, **kwargs):
        self.id: str = id
        self.name: str = name
        self.description: str = description
        self.labels: List[Label] = labels
        self.created_at: datetime = created_at
        self.modified_at: datetime = modified_at

    def __eq__(self, other):
        if not isinstance(other, Scenario):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return "Scenario id: " + str(self.id) + ", Scenario description: " + str(self.description)

    @staticmethod
    def from_dict(scenario_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.scenario.Scenario` object, created from the values in the dict
        provided as parameter

        :param scenario_dict: Dict which includes the necessary values to create the object
        :type scenario_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.scenario.Scenario`
        """
        scenario_dict['created_at'] = parse_datetime(scenario_dict['created_at'])
        scenario_dict['modified_at'] = parse_datetime(scenario_dict['modified_at'])
        if scenario_dict.get('labels'):
            scenario_dict['labels'] = [Label.from_dict(l) for l in scenario_dict['labels']]
        return Scenario(**scenario_dict)
