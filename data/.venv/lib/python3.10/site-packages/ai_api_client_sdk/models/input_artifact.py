from typing import Any, Dict, List

from ai_api_client_sdk.models.artifact import Artifact
from ai_api_client_sdk.models.label import Label


class InputArtifact:
    """The InputArtifact object defines the input artifact specified in the executable definition.
    :param name: name of artifact
    :type name: str
    :param kind: kind of artifact (Dataset, Model, ResultSet)
    :type kind: str
    :param description: description of artifact
    :type description: str
    :param labels: labels for artifact
    :type labels: List[class:`ai_api_client_sdk.models.label.Label`]
    """

    def __str__(self):
        return "Input artifact name: " + str(self.name) + ", Input artifact kind: " + str(self.kind) + \
               ", Input artifact description: " + str(self.description)

    def __eq__(self, other):
        if not isinstance(other, InputArtifact):
            return False
        return self.name == other.name and self.kind == other.kind and self.description == other.description and \
            self.labels == other.labels

    def __init__(self, name: str, kind: str = None, description: str = None, labels: List[Label] = None):
        self.name: str = name
        self.kind: str = kind
        self.description: str = description
        self.labels: List[Label] = labels

    @staticmethod
    def from_dict(input_artifact_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.input_artifact.InputArtifact` object, created from the values
        in the dict provided as parameter

        :param input_artifact_dict: Dict which includes the necessary values to create the object
        :type input_artifact_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.input_artifact.InputArtifact`
        """
        if input_artifact_dict.get('labels'):
            input_artifact_dict['labels'] = [Label.from_dict(l) for l in input_artifact_dict['labels']]
        return InputArtifact(**input_artifact_dict)
