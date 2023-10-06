from ai_api_client_sdk.models.capabilities import Capabilities
from ai_api_client_sdk.models.version_list import VersionList
from ai_api_client_sdk.resource_clients.base_client import BaseClient


class MetaClient(BaseClient):

    def get(self) -> Capabilities:
        capabilities_dict = self.rest_client.get(path='/meta')
        return Capabilities.from_dict(capabilities_dict)

    def get_versions(self) -> VersionList:
        version_list_dict = self.rest_client.get(path='/meta/versions')
        return VersionList.from_dict(version_list_dict)
