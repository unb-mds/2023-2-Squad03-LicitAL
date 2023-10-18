from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime
from ai_api_client_sdk.models.label import Label
from ai_api_client_sdk.models.scenario import Scenario


class Artifact:
    """The Artifact object defines an artifact

    :param name: Name of the artifact
    :type name: str
    :param id: ID of the artifact
    :type id: str
    :param url: URL of the artifact
    :type url: str
    :param kind: Kind of the artifact
    :type kind: class:`ai_api_client_sdk.models.artifact.Artifact.Kind`
    :param scenario_id: ID of the scenario which the artifact belongs to
    :type scenario_id: str
    :param created_at: Time when the artifact was created
    :type created_at: datetime
    :param modified_at: Time when the artifact was last modified
    :type modified_at: datetime
    :param execution_id: ID of the execution which the artifact resulted from, defaults to None
    :type execution_id: str, optional
    :param configuration_id: ID of the configuration which the artifact relates to, defaults to None
    :type configuration_id: str, optional
    :param description: Description of the artifact, defaults to None
    :type description: str, optional
    :param labels: List of the labels of the artifact, defaults to None
    :type labels: List[class:`ai_api_client_sdk.models.label.Label`]
    :param scenario: A dict, which gives detailed information on scenario, defaults to None
    :type scenario: class:`ai_api_client_sdk.models.scenario.Scenario`, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """

    class Kind(Enum):
        MODEL = 'model'
        DATASET = 'dataset'
        RESULTSET = 'resultset'
        OTHER = 'other'

    def __init__(self, name: str, id: str, url: str, kind: Kind, scenario_id: str, created_at: datetime,
                 modified_at: datetime, execution_id: str = None, configuration_id: str = None, description: str = None,
                 labels: List[Label] = None, scenario:Scenario = None, **kwargs):
        self.id: str = id
        self.name: str = name
        self.url: str = url
        self.kind: Artifact.Kind = kind  # pylint: disable=used-before-assignment
        self.description: str = description
        self.scenario_id: str = scenario_id
        self.execution_id: str = execution_id
        self.configuration_id: str = configuration_id
        self.labels: List[Label] = labels
        self.created_at: datetime = created_at
        self.modified_at: datetime = modified_at
        self.scenario: Scenario = scenario

    def __eq__(self, other):
        if not isinstance(other, Artifact):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return "Artifact id: " + str(self.id) + ", Artifact description: " + str(self.description)

    @staticmethod
    def from_dict(artifact_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.artifact.Artifact` object, created from the values in the dict
        provided as parameter

        :param artifact_dict: Dict which includes the necessary values to create the object
        :type artifact_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.artifact.Artifact`
        """
        artifact_dict['kind'] = Artifact.Kind(artifact_dict['kind'])
        artifact_dict['created_at'] = parse_datetime(artifact_dict['created_at'])
        artifact_dict['modified_at'] = parse_datetime(artifact_dict['modified_at'])
        if artifact_dict.get('labels'):
            artifact_dict['labels'] = [Label.from_dict(l) for l in artifact_dict['labels']]
        if artifact_dict.get('scenario'):
            artifact_dict['scenario'] = Scenario.from_dict(artifact_dict['scenario'])
        return Artifact(**artifact_dict)
