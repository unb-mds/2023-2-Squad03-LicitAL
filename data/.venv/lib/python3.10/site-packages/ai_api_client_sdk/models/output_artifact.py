from typing import Any, Dict, List

from ai_api_client_sdk.models.artifact import Artifact
from ai_api_client_sdk.models.label import Label


class OutputArtifact:
    """The OutputArtifact object defines the output artifact specified in the executable definition.
    :param name: name of artifact
    :type name: str
    :param kind: kind of artifact (Dataset, Model, ResultSet)
    :type kind: str
    :param description: description of artifact
    :type description: str
    :param labels: labels for artifact
    :type labels: List[class:`ai_api_client_sdk.models.label.Label`]
    """
    def __init__(self, name: str, kind: str = None, description: str = None, labels: List[Label] = None):
        self.name: str = name
        self.kind: str = kind
        self.description: str = description
        self.labels: List[Label] = labels

    def __str__(self):
        return "Output artifact name: " + str(self.name) + ", Output artifact kind: " + str(self.kind) + \
               ", Output artifact description: " + str(self.description)

    def __eq__(self, other):
        if not isinstance(other, OutputArtifact):
            return False
        return self.name == other.name and self.kind == other.kind and self.description == other.description and \
            self.labels == other.labels

    @staticmethod
    def from_dict(output_artifact_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.output_artifact.OutputArtifact` object, created from the values
        in the dict provided as parameter

        :param output_artifact_dict: Dict which includes the necessary values to create the object
        :type output_artifact_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.output_artifact.OutputArtifact`
        """
        if output_artifact_dict.get('labels'):
            output_artifact_dict['labels'] = [Label.from_dict(l) for l in output_artifact_dict['labels']]
        return OutputArtifact(**output_artifact_dict)
