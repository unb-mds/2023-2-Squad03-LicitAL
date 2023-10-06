from typing import Dict


class InputArtifactBinding:
    """The InputArtifactBinding object defines the input artifact specified in the configuration.

    :param key: matches the input artifact name in the executable definition
    :type key: str
    :param id: ID of the artifact
    :type id: str
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, key: str, artifact_id: str, **kwargs):
        self.key: str = key
        self.artifact_id: str = artifact_id

    def to_dict(self) -> Dict[str, str]:
        """Returns the attributes of the object as a dictionary

        :return: A dict, including all the attributes of the object
        :rtype: Dict[str, str]
        """
        return {'key': self.key, 'artifact_id': self.artifact_id}

    def __eq__(self, other):
        if not isinstance(other, InputArtifactBinding):
            return False
        return self.key == other.key and self.artifact_id == other.artifact_id

    @staticmethod
    def from_dict(input_artifact_binding_dict: Dict[str, str]):
        """Returns a :class:`ai_api_client_sdk.models.input_artifact_binding.InputArtifactBinding` object, created from
        the values in the dict provided as parameter

        :param input_artifact_binding_dict: Dict which includes the necessary values to create the object
        :type input_artifact_binding_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_api_client_sdk.models.input_artifact_binding.InputArtifactBinding`
        """
        return InputArtifactBinding(**input_artifact_binding_dict)
