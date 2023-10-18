from typing import Dict

from ai_core_sdk.models import Name


class DockerRegistrySecret(Name):
    """The DockerRegistrySecret object defines the docker registry secret. Refer to
    :class:`ai_api_client_sdk.models.base_models.Name`, for the object definition
    """
    def __str__(self):
        return "DockerRegistrySecret name: " + str(self.name)

    @staticmethod
    def from_dict(docker_registry_secret_dict: Dict[str, str]):
        """Returns a :class:`ai_core_sdk.models.docker_registry_secret.DockerRegistrySecret` object, created
        from the values in the dict provided as parameter

        :param docker_registry_secret_dict: Dict which includes the necessary values to create the object
        :type docker_registry_secret_dict: Dict[str, str]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.docker_registry_secret.DockerRegistrySecret`
        """
        return DockerRegistrySecret(**docker_registry_secret_dict)
