import json
import re

from metaflow import current, decorators, parameters, JSONType
from metaflow.metaflow_config import from_conf
from metaflow.package import MetaflowPackage
from metaflow.exception import MetaflowException
from metaflow._vendor import click


class InvalidArgoName(MetaflowException):
    headline = "Invalid Argo workflow template name"


@click.group()
def cli():
    """
    Defines an argo group
    """


@cli.group(help="Commands related to Argo Workflows.")
@click.option(
    "--name",
    default=None,
    type=str,
    help="Workflow Template name. The flow name is used instead "
    "if this option is not specified.",
)
@click.pass_obj
def argo(obj, name=None):
    obj.check(obj.graph, obj.flow, obj.environment, pylint=obj.pylint)
    obj.workflow_template_name = resolve_workflow_template_name(name)


@argo.command(help="Deploy a new version of this workflow to Argo Workflow Templates.")
@click.option(
    "--image-pull-secret",
    "image_pull_secrets",
    default=None,
    multiple=True,
    help="Docker image pull secret.",
)
@click.option(
    "--label",
    "labels",
    multiple=True,
    default=None,
    help="Label to attach to the workflow template.",
)
@click.option(
    "--annotation",
    "annotations",
    multiple=True,
    default=None,
    help="Annotation to attach to the workflow template.",
)
@click.option(
    "--volume-claim",
    "volume_claim",
    default=50000,
    type=int,
    help="Size of the volumeClaim in MiB",
)
@click.option(
    "--k8s-namespace",
    "k8s_namespace",
    default=None,
    help="Deploy into the specified kubernetes namespace.",
)
@click.option('--embedded',
              is_flag=True,
              default=False,
              help="Don't download code package into step containers."
                   "Docker images should have a flow and all dependencies embedded."
)
@click.option(
    "--max-workers",
    default=100,
    type=int,
    show_default=True,
    help="Maximum number of parallel pods.",
)
@click.option(
    "--workflow-timeout", default=None, type=int, help="Workflow timeout in seconds."
)
@click.option(
    "--only-json",
    is_flag=True,
    default=False,
    help="Only print out JSON sent to Argo. Do not deploy anything.",
)
@click.pass_obj
def create(
    obj,
    image_pull_secrets,
    labels,
    annotations,
    volume_claim,
    k8s_namespace,
    embedded,
    max_workers,
    workflow_timeout=None,
    only_json=False,
):
    obj.echo(
        "Deploying *%s* to Argo Workflow Templates..." % obj.workflow_template_name,
        bold=True,
    )

    from .argo_workflow import ArgoWorkflow
    from metaflow.plugins.kubernetes.kubernetes_decorator import KubernetesDecorator

    if obj.flow_datastore.TYPE != "s3":
        raise MetaflowException("Argo Workflows require --datastore=s3.")

    # When using conda attach Kubernetes decorator to the flow.
    # This results in 'linux-64' libraries to be packaged.
    decorators._attach_decorators(obj.flow, [KubernetesDecorator.name])
    decorators._init_step_decorators(
        obj.flow, obj.graph, obj.environment, obj.flow_datastore, obj.logger
    )

    obj.package = MetaflowPackage(
        obj.flow, obj.environment, obj.echo, obj.package_suffixes
    )
    package_url, _ = obj.flow_datastore.save_data([obj.package.blob], len_hint=1)[0]

    workflow = ArgoWorkflow(
        obj.workflow_template_name,
        obj.flow,
        obj.graph,
        obj.package,
        package_url if not embedded else None,
        obj.metadata,
        obj.flow_datastore,
        obj.environment,
        obj.event_logger,
        obj.monitor,
        image_pull_secrets,
        labels,
        annotations,
        volume_claim,
        max_workers,
        workflow_timeout,
    )

    if only_json:
        obj.echo_always(workflow.to_json(), err=False, no_bold=True, nl=False)
    else:
        workflow.deploy(k8s_namespace)
        obj.echo(
            "WorkflowTemplate *{name}* is pushed to Argo Workflows successfully.\n".format(
                name=obj.workflow_template_name
            ),
            bold=True,
        )
        workflow.schedule(k8s_namespace)
        obj.echo("What will trigger execution of the workflow:", bold=True)
        obj.echo(workflow.trigger_explanation(), indent=True)


@parameters.add_custom_parameters(deploy_mode=False)
@argo.command(help="Trigger the workflow from the Argo Workflow Template.")
@click.option(
    "--k8s-namespace",
    "k8s_namespace",
    default=None,
    help="Submit the Workflow in the specified kubernetes namespace.",
)
@click.pass_obj
def trigger(obj, k8s_namespace, **kwargs):
    from .argo_workflow import ArgoWorkflow

    def _convert_value(param):
        v = kwargs.get(param.name)
        if param.kwargs.get("type") == JSONType:
            return json.dumps(v)
        if callable(v):
            return v()
        return v

    params = {
        p.name: _convert_value(p)
        for _, p in obj.flow._get_parameters()
        if kwargs.get(p.name) is not None
    }
    response = ArgoWorkflow.trigger(k8s_namespace, obj.workflow_template_name, params)
    run_id = response["metadata"]["name"]
    obj.echo(
        "Workflow *{name}* is triggered on Argo Workflows (run-id *{id}*).".format(
            name=obj.workflow_template_name, id=run_id
        ),
        bold=True,
    )


@argo.command(help="List workflows on Argo Workflows.")
@click.pass_obj
@click.option(
    "--k8s-namespace",
    "k8s_namespace",
    default=None,
    help="List workflows in the specified kubernetes namespace.",
)
@click.option(
    "--pending",
    default=False,
    is_flag=True,
    help="List workflows in the 'Pending' state on Argo Workflows.",
)
@click.option(
    "--running",
    default=False,
    is_flag=True,
    help="List workflows in the 'Running' state on Argo Workflows.",
)
@click.option(
    "--succeeded",
    default=False,
    is_flag=True,
    help="List workflows in the 'Succeeded' state on Argo Workflows.",
)
@click.option(
    "--failed",
    default=False,
    is_flag=True,
    help="List workflows in the 'Failed' state on Argo Workflows.",
)
@click.option(
    "--error",
    default=False,
    is_flag=True,
    help="List workflows in the 'Error' state on Argo Workflows.",
)
def list_runs(obj, k8s_namespace, pending, running, succeeded, failed, error):
    from .argo_workflow import ArgoWorkflow

    states = []
    if pending:
        states.append("Pending")
    if running:
        states.append("Running")
    if succeeded:
        states.append("Succeeded")
    if failed:
        states.append("Failed")
    if error:
        states.append("Error")

    workflows = ArgoWorkflow.list(k8s_namespace, obj.workflow_template_name, states)
    workflows = sorted(workflows, key=lambda w: w["status"]["startedAt"], reverse=True)
    if not workflows:
        if states:
            status = ",".join(["*%s*" % s for s in states])
            obj.echo(
                "No %s workflows for *%s* found on Argo Workflows."
                % (status, obj.workflow_template_name)
            )
        else:
            obj.echo(
                "No workflows for *%s* found on Argo Workflows."
                % (obj.workflow_template_name)
            )
        return
    for wf in workflows:
        if wf["status"].get("finishedAt"):
            obj.echo(
                "*{id}* "
                "startedAt:'{startedAt}' "
                "stoppedAt:'{finishedAt}' "
                "*{status}*".format(
                    id=wf["metadata"]["name"],
                    status=wf["status"]["phase"],
                    startedAt=wf["status"]["startedAt"],
                    finishedAt=wf["status"]["finishedAt"],
                )
            )
        else:
            obj.echo(
                "*{id}* "
                "startedAt:'{startedAt}' "
                "*{status}*".format(
                    id=wf["metadata"]["name"],
                    status=wf["status"]["phase"],
                    startedAt=wf["status"]["startedAt"],
                )
            )


def resolve_workflow_template_name(name):
    """
    Returns a valid workflow template name.
    """
    from .argo_workflow import dns_name

    if name is None:
        name = dns_name(current.flow_name)

    prefix = from_conf("ARGO_WORKFLOW_PREFIX")
    if prefix:
        name = prefix + "-" + name

    if not re.match("^[a-z0-9]([-.a-z0-9]*[a-z0-9])?$", name):
        raise InvalidArgoName(
            "Invalid workflow template name: *%s*.\n"
            "See https://kubernetes.io/docs/concepts/overview/working-with-objects/names/"
            % name
        )
    return name
