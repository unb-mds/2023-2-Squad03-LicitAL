from typing import Callable

from ai_api_client_sdk.exception import AIAPIAuthenticatorException
from ai_api_client_sdk.helpers.authenticator import Authenticator
from ai_api_client_sdk.helpers.rest_client import RestClient
from ai_api_client_sdk.resource_clients import ArtifactClient, ConfigurationClient, DeploymentClient, \
    ExecutableClient, ExecutionClient, ExecutionScheduleClient, HealthzClient, MetaClient, MetricsClient, \
    ScenarioClient, ResourceGroupsClient
from ai_api_client_sdk.helpers.constants import Timeouts


class AIAPIV2Client:
    """The AIAPIV2Client is the class implemented to interact with the AI API server. The user can use its attributes
    corresponding to the resources, for interacting with endpoints related to that resource. (i.e.,
    aiapiv2client.scenario)

    :param base_url: Base URL of the AI API server. Should include the base path as well. (i.e., "<base_url>/scenarios"
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
        if not token_creator:
            if not (auth_url and client_id and client_secret):
                raise AIAPIAuthenticatorException(
                    error_message='Either token_creator or auth_url & client_id & client_secret should be provided')
            token_creator = Authenticator(auth_url=auth_url, client_id=client_id, client_secret=client_secret).get_token
        self.rest_client: RestClient = RestClient(base_url=base_url, get_token=token_creator,
                                                  resource_group=resource_group, read_timeout=read_timeout,
                                                  connect_timeout=connect_timeout,
                                                  num_request_retries=num_request_retries,
                                                  client_type='AI API Python SDK')
        self.artifact: ArtifactClient = ArtifactClient(rest_client=self.rest_client)
        self.configuration: ConfigurationClient = ConfigurationClient(rest_client=self.rest_client)
        self.deployment: DeploymentClient = DeploymentClient(rest_client=self.rest_client)
        self.executable: ExecutableClient = ExecutableClient(rest_client=self.rest_client)
        self.execution: ExecutionClient = ExecutionClient(rest_client=self.rest_client)
        self.execution_schedule: ExecutionScheduleClient = ExecutionScheduleClient(rest_client=self.rest_client)
        self.healthz: HealthzClient = HealthzClient(rest_client=self.rest_client)
        self.metrics: MetricsClient = MetricsClient(rest_client=self.rest_client)
        self.scenario: ScenarioClient = ScenarioClient(rest_client=self.rest_client)
        self.meta: MetaClient = MetaClient(rest_client=self.rest_client)
        admin_rest_client = RestClient(base_url=base_url[:-3], get_token=token_creator, resource_group=resource_group)
        self.resource_groups: ResourceGroupsClient = ResourceGroupsClient(rest_client=admin_rest_client)
