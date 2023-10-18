from typing import Callable
import os

from ai_core_sdk.exception import AIAPIAuthenticatorException
from ai_core_sdk.helpers import Authenticator, is_within_aicore
from ai_core_sdk.resource_clients import AIAPIV2Client, ArtifactClient, ConfigurationClient, DeploymentClient, \
    ExecutableClient, ExecutionClient, RestClient, ScenarioClient, ResourceGroupsClient, MetaClient
from ai_core_sdk.resource_clients.applications_client import ApplicationsClient
from ai_core_sdk.resource_clients.docker_registry_secrets_client import DockerRegistrySecretsClient
from ai_core_sdk.resource_clients.metrics_client import MetricsCoreClient
from ai_core_sdk.resource_clients.object_store_secrets_client import ObjectStoreSecretsClient
from ai_core_sdk.resource_clients.kpi_client import KpiClient
from ai_core_sdk.resource_clients.repositories_client import RepositoriesClient
from ai_core_sdk.resource_clients.secrets_client import SecretsClient
from ai_core_sdk.helpers.constants import Timeouts


class AICoreV2Client:
    """The AICoreV2Client is the class implemented to interact with the AI Core endpoints. The user can use its
    attributes corresponding to the resources, for interacting with endpoints related to that resource. (i.e.,
    aicoreclient.scenario)

    :param base_url: Base URL of the AI Core. Should include the base path as well. (i.e., "<base_url>/lm/scenarios"
        should work)
    :type base_url: str
    :param auth_url: URL of the authorization endpoint. Should be the full URL (including /oauth/token), defaults to
        None
    :type auth_url: str, optional
    :param client_id: client id to be used for authorization, defaults to None
    :type client_id: str, optional
    :param client_secret: client secret to be used for authorization, defaults to None
    :type client_secret: str, optional
    :param token_creator: the function which returns the Bearer token, when called. Either this, or
        auth_url & client_id & client_secret should be specified, defaults to None
    :type token_creator: Callable[[], str], optional
    :param resource_group: The default resource group which will be used while sending the requests to the server. If
        not set, the resource_group should be specified with every request to the server, defaults to None
    :type resource_group: str, optional
    :param read_timeout: Read timeout for requests in seconds, defaults to 60s
    :type read_timeout: int
    :param connect_timeout: Connect timeout for requests in seconds, defaults to 60s
    :type connect_timeout: int
    :param num_request_retries: Number of retries for failing requests with http status code 429, 500, 502, 503 or 504,
        defaults to 60s
    :type num_request_retries: int
    """
    def __init__(self, base_url: str, auth_url: str = None, client_id: str = None, client_secret: str = None,
                 token_creator: Callable[[], str] = None, resource_group: str = None,
                 read_timeout=Timeouts.READ_TIMEOUT.value, connect_timeout=Timeouts.CONNECT_TIMEOUT.value,
                 num_request_retries=Timeouts.NUM_REQUEST_RETRIES.value):
        self.base_url: str = base_url
        ai_api_base_url = f'{base_url}/lm'

        # If the environment variables have AICORE_EXECUTION_ID and AICORE_TRACKING_ENDPOINT,
        # it indicates the sdk is used within the training pod
        if is_within_aicore():
            api_base_url = os.getenv('AICORE_TRACKING_ENDPOINT')
            # framing the base url of tracking endpoint
            base_url = f'{api_base_url}/api/v1'
            # dummy token creator function to be passed to rest client
            def dummy_token_creator():
                return ''
            token_creator = dummy_token_creator
            # resource group will be auto detected from the request going to tracking api from the training pod.
            # Hence not passing the resource group id
            resource_group = ''

        if not token_creator:
            if not (auth_url and client_id and client_secret):
                raise AIAPIAuthenticatorException(
                    'Either token_creator or auth_url & client_id & client_secret should be provided')
            token_creator = Authenticator(auth_url=auth_url, client_id=client_id, client_secret=client_secret).get_token
        ai_api_v2_client = AIAPIV2Client(base_url=ai_api_base_url, auth_url=auth_url, token_creator=token_creator,
                                         resource_group=resource_group, read_timeout=read_timeout,
                                         connect_timeout=connect_timeout, num_request_retries=num_request_retries)
        self.rest_client: RestClient = RestClient(base_url=base_url, get_token=token_creator,
                                                  resource_group=resource_group, read_timeout=read_timeout,
                                                  connect_timeout=connect_timeout,
                                                  num_request_retries=num_request_retries,
                                                  client_type='AI Core Python SDK')
        self.artifact: ArtifactClient = ai_api_v2_client.artifact
        self.configuration: ConfigurationClient = ai_api_v2_client.configuration
        self.deployment: DeploymentClient = ai_api_v2_client.deployment
        self.executable: ExecutableClient = ai_api_v2_client.executable
        self.execution: ExecutionClient = ai_api_v2_client.execution
        self.resource_groups: ResourceGroupsClient = ai_api_v2_client.resource_groups
        self.meta: MetaClient = ai_api_v2_client.meta
        # If the environment variables have AICORE_EXECUTION_ID and AICORE_TRACKING_ENDPOINT,
        # it indicates the sdk is used within the training pod
        # Initiating the normal rest client if within the training pod
        # Else initiating the rest client from ai_api_v2_client
        if is_within_aicore():
            self.metrics: MetricsCoreClient = MetricsCoreClient(rest_client=self.rest_client,
                                                                execution_id=os.getenv('AICORE_EXECUTION_ID'))
        else:
            self.metrics: MetricsCoreClient = MetricsCoreClient(rest_client=ai_api_v2_client.rest_client)
        self.scenario: ScenarioClient = ai_api_v2_client.scenario
        self.docker_registry_secrets: DockerRegistrySecretsClient = DockerRegistrySecretsClient(
            rest_client=self.rest_client)
        self.applications: ApplicationsClient = ApplicationsClient(rest_client=self.rest_client)
        self.object_store_secrets: ObjectStoreSecretsClient = ObjectStoreSecretsClient(rest_client=self.rest_client)
        self.secrets: SecretsClient = SecretsClient(rest_client=self.rest_client)
        self.kpis: KpiClient = KpiClient(rest_client=self.rest_client)
        self.repositories: RepositoriesClient = RepositoriesClient(rest_client=self.rest_client)
