from typing import List

from ai_api_client_sdk.models.artifact import Artifact
from ai_api_client_sdk.models.artifact_create_response import ArtifactCreateResponse
from ai_api_client_sdk.models.artifact_query_response import ArtifactQueryResponse
from ai_api_client_sdk.models.label import Label
from ai_api_client_sdk.resource_clients.base_client import BaseClient


class ArtifactClient(BaseClient):
    """ArtifactClient is a class implemented for interacting with the artifact related endpoints of the server. It
    implements the base class :class:`ai_api_client_sdk.resource_clients.base_client.BaseClient`
    """

    def create(self, name: str, kind: Artifact.Kind, url: str, scenario_id: str, description: str = None,
               labels: List[Label] = None, resource_group: str = None) -> ArtifactCreateResponse:
        """Creates an artifact.

        :param name: Name of the artifact
        :type name: str
        :param kind: Kind of the artifact
        :type kind: class:`ai_api_client_sdk.models.artifact.Artifact.Kind`
        :param url: URL of the artifact
        :type url: str
        :param scenario_id: ID of the scenario which the artifact should belong to
        :type scenario_id: str
        :param description: Description of the artifact, defaults to None
        :type description: str, optional
        :param labels: List of the labels of the artifact, defaults to None
        :type labels: List[class:`ai_api_client_sdk.models.label.Label`]
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.artifact_create_response.ArtifactCreateResponse`
        """
        body = {
            'name': name,
            'kind': kind.value,
            'url': url,
            'scenario_id': scenario_id
        }
        if description:
            body['description'] = description
        if labels:
            body['labels'] = [l.to_dict() for l in labels]
        response_dict = self.rest_client.post(path='/artifacts', body=body, resource_group=resource_group)
        return ArtifactCreateResponse.from_dict(response_dict)

    def get(self, artifact_id: str, expand: str = None, resource_group: str = None) -> Artifact:
        """Retrieves the artifact from the server.

        :param artifact_id: ID of the artifact to be retrieved
        :type artifact_id: str
        :param expand: Entity whose details to be displayed in the response, defaults to None
        :type expand: str, optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPINotFoundException` if a 404 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: The retrieved artifact
        :rtype: class:`ai_api_client_sdk.models.artifact.Artifact`
        """
        params = self._form_query_params(expand=expand)
        artifact_dict = self.rest_client.get(path=f'/artifacts/{artifact_id}', params=params,
                                             resource_group=resource_group)
        return Artifact.from_dict(artifact_dict)

    def query(self, scenario_id: str = None, execution_id: str = None, name: str = None, kind: Artifact.Kind = None,
              artifact_label_selector: List[str] = None, top: int = None, skip: int = None, search: str = None,
              search_case_insensitive: bool = None, expand: str = None,
              resource_group: str = None) -> ArtifactQueryResponse:
        """Queries the artifacts.

        :param scenario_id: ID of the scenario the artifacts should belong to, defaults to None
        :type scenario_id: str, optional
        :param execution_id: ID of the execution the artifact should be resulted from, defaults to None
        :type execution_id: str, optional
        :param name: Name of the artifact(s) to be retrieved, defaults to None
        :type name: str, optional
        :param kind: Kind of the artifacts to be retrieved, defaults to None
        :type kind: class:`ai_api_client_sdk.models.artifact.Artifact.Kind`, optional
        :param artifact_label_selector: Query the artifacts based on their labels in the form of "key=value" or
            "key!=value" separated by commas, defaults to None
        :type artifact_label_selector: list, optional
        :param top: Number of artifacts to be retrieved, defaults to None
        :type top: int, optional
        :param skip: Number of artifacts to be skipped, from the list of the queried artifacts, defaults to None
        :type skip: int, optional
        :param search: Generic search term to be looked for in various attributes of artifacts, defaults to None
        :type search: str, optional
        :param search_case_insensitive: Indicates whether the search should be case insensitive
        :type search_case_insensitive: bool, optional
        :param expand: Entity whose details to be displayed in the response, defaults to None
        :type expand: str, optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: class:`ai_api_client_sdk.models.artifact_query_response.ArtifactQueryResponse`
        """
        params = self._form_query_params(scenario_id=scenario_id, execution_id=execution_id, name=name, top=top,
                                         skip=skip, artifact_label_selector=artifact_label_selector, search=search,
                                         search_case_insensitive=search_case_insensitive, expand=expand,
                                         kind=kind.value if kind else None)
        response_dict = self.rest_client.get(path='/artifacts', params=params, resource_group=resource_group)
        return ArtifactQueryResponse.from_dict(response_dict)

    def count(self, scenario_id: str = None, execution_id: str = None, name: str = None, kind: Artifact.Kind = None,
              artifact_label_selector: List[str] = None, resource_group: str = None) -> int:
        """Counts the artifacts.

        :param scenario_id: ID of the scenario the artifacts should belong to, defaults to None
        :type scenario_id: str, optional
        :param execution_id: ID of the execution the artifact should be resulted from, defaults to None
        :type execution_id: str, optional
        :param name: Name of the artifact(s) to be retrieved, defaults to None
        :type name: str, optional
        :param kind: Kind of the artifacts to be retrieved, defaults to None
        :type kind: class:`ai_api_client_sdk.models.artifact.Artifact.Kind`, optional
        :param artifact_label_selector: list of the label selector strings in the form of "key=value" or "key!=value", to filter
            the artifacts with respect to their labels, defaults to None
        :type artifact_label_selector: List[str], optional
        :param resource_group: Resource Group which the request should be sent on behalf. Either this or a default
            resource group in the :class:`ai_api_client_sdk.ai_api_v2_client.AIAPIV2Client` should be specified,
            defaults to None
        :type resource_group: str
        :raises: class:`ai_api_client_sdk.exception.AIAPIInvalidRequestException` if a 400 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIAuthorizationException` if a 401 response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIServerException` if a non-2XX response is received from the
            server
        :raises: class:`ai_api_client_sdk.exception.AIAPIRequestException` if an unexpected exception occurs while
            trying to send a request to the server
        :return: An object representing the response from the server
        :rtype: int
        """
        params = self._form_query_params(scenario_id=scenario_id, execution_id=execution_id, name=name,
                                         kind=kind.value if kind else None,
                                         artifact_label_selector=artifact_label_selector)
        return self.rest_client.get(path='/artifacts/$count', params=params, resource_group=resource_group)
