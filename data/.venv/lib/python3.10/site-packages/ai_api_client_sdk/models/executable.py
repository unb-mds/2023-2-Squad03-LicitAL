from datetime import datetime
from typing import Any, Dict, List

from ai_api_client_sdk.helpers.datetime_parser import parse_datetime
from ai_api_client_sdk.models.input_artifact import InputArtifact
from ai_api_client_sdk.models.label import Label
from ai_api_client_sdk.models.parameter import Parameter
from ai_api_client_sdk.models.output_artifact import OutputArtifact


class Executable:
    """The Executable object defines an executable
    :param id: ID of the Executable
    :type id: str
    :param scenario_id: ID of the scenario which the executable belongs to
    :type scenario_id: str
    :param version_id: ID of the version of the scenario, the executable belongs to
    :type version_id: str
    :param name: Name of the executable
    :type name: str
    :param deployable: Flag which defines if the executable is deployable
    :type deployable: bool
    :param created_at: Time when the executable was created
    :type created_at: datetime
    :param modified_at: Time when the executable was last modified
    :type modified_at: datetime
    :param description: Description of the executable, defaults to None
    :type description: str, optional
    :param parameters: List of the parameters of the executable, defaults to None
    :type parameters: List[class:`ai_api_client_sdk.models.parameter.Parameter`], optional
    :param input_artifacts: List of the input artifacts which are to be used by the executable, defaults to None
    :type input_artifacts: List[class:`ai_api_client_sdk.models.input_artifact.InputArtifact`], optional
    :param output_artifacts: List of the artifacts to be created by the executable, defaults to None
    :type output_artifacts: List[class:`ai_api_client_sdk.models.output_artifact.OutputArtifact`], optional
    :param labels: List of the labels of the executable, defaults to None
    :type labels: List[class:`ai_api_client_sdk.models.label.Label`]
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, id: str, scenario_id: str, version_id: str, name: str, deployable: bool, created_at: datetime,
                 modified_at: datetime, description: str = None, parameters: List[Parameter] = None,
                 input_artifacts: List[InputArtifact] = None, output_artifacts: List[OutputArtifact] = None,
                 labels: List[Label] = None, **kwargs):
        self.id: str = id
        self.scenario_id: str = scenario_id
        self.version_id: str = version_id
        self.name: str = name
        self.description: str = description
        self.deployable: bool = deployable
        self.parameters: List[Parameter] = parameters
        self.input_artifacts: List[InputArtifact] = input_artifacts
        self.output_artifacts: List[OutputArtifact] = output_artifacts
        self.labels: List[Label] = labels
        self.created_at: datetime = created_at
        self.modified_at: datetime = modified_at

    def __eq__(self, other):
        if not isinstance(other, Executable):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return "Executable id: " + str(self.id) + ", Executable description: " + str(self.description)

    @staticmethod
    def from_dict(executable_dict: Dict[str, Any]):
        """Returns a :class:`ai_api_client_sdk.models.executable.Executable` object, created from the values in the dict
        provided as parameter

        :param executable_dict: Dict which includes the necessary values to create the object
        :type executable_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.executable.Executable`
        """
        executable_dict['created_at'] = parse_datetime(executable_dict['created_at'])
        executable_dict['modified_at'] = parse_datetime(executable_dict['modified_at'])
        if executable_dict.get('parameters'):
            executable_dict['parameters'] = [Parameter.from_dict(p) for p in executable_dict['parameters']]
        if executable_dict.get('input_artifacts'):
            executable_dict['input_artifacts'] = \
                [InputArtifact.from_dict(ia) for ia in executable_dict['input_artifacts']]
        if executable_dict.get('output_artifacts'):
            executable_dict['output_artifacts'] = \
                [OutputArtifact.from_dict(oa) for oa in executable_dict['output_artifacts']]
        if executable_dict.get('labels'):
            executable_dict['labels'] = [Label.from_dict(l) for l in executable_dict['labels']]
        return Executable(**executable_dict)
