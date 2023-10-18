import pathlib
import shutil

import click
import yaml

from .content_package import get_content_packages
from .print_utils import print_content_package, print_workflow


def _get_workflow_from_cfg(
    workflow_config, package_key=".contentPackage", workflow_key=".workflow"
):
    if not isinstance(workflow_config, dict):
        with pathlib.Path(workflow_config).open() as stream:
            workflow_config = yaml.safe_load(stream)
    package_name = workflow_config.get(package_key, None)
    workflow_name = workflow_config.get(workflow_key, None)
    if package_name and workflow_name:
        return package_name, workflow_name, workflow_config
    else:
        raise click.ClickException(
            f'Keys "{package_key}" and "{workflow_key}" are expected in the workflow config.'
        )


def _get_package_or_workflow_obj(content_packages, package, workflow=None):
    try:
        ret = content_packages[package]
    except KeyError:
        raise click.ClickException(
            f'No content package "{package}". Run `aicore-content list` to list installed packages.'
        )

    if workflow:
        try:
            ret = ret.workflows[workflow]
        except KeyError:
            raise click.ClickException(
                f'No workflow "{workflow}" in content package "{package}". Run `aicore-content list {package}` to list available workflows.'
            )

    return ret


HELP_STRINGS = {
    "dry-run": "echo commands instead of executing it",
    "package": "set/overwrite .contentPackage key in the workflow config to select a content package",
    "workflow": "set/overwrite .workflow key in the workflow config to select a workflow",
}


@click.group()
@click.option(
    "--content-pkg-definition",
    "-c",
    "content_spec",
    type=click.Path(exists=True),
    multiple=True,
    help="paths to additional content package definitions.",
)
@click.pass_context
def cli(ctx, content_spec):
    """CLI to discover and consume content packages for AI Core."""
    ctx.ensure_object(dict)
    try:
        ctx.obj["content_packages"] = get_content_packages(content_spec)
    except Exception as err:
        raise click.ClickException(f"Loading content package\n{err}")


def _list_single_content_package(package):
    for workflow in package.workflows.values():
        try:
            print_workflow(workflow, compact=True)
        except Exception as err:
            raise click.ClickException(f'Workflow details could not be retrieved:\n{err}')
        else:
            click.echo("\n")


def _list_content_packages(content_packages):
    for pkg in content_packages.values():
        try:
            print_content_package(pkg, compact=True)
        except Exception as err:
            raise click.ClickException(f'Content Package details could not be retrieved:\n{err}')
        else:
            click.echo("\n")


def _list_workflow(workflow):
    click.echo(f"Workflow {workflow.name} avaiable docker types:")
    for n in workflow.dockerfiles.keys():
        click.echo(f"\t- {n}")


@cli.command(name="list")
@click.pass_context
@click.argument("package", required=False, default=None)
@click.argument("workflow", required=False, default=None)
def _list(ctx, package, workflow):
    """List content packages/workflows/dockerfiles.

    Without arguments, this command prints a list of available packages.

    PACKAGE [optional] Name of the content package. If provided this command prints a list of the workflows in the package.
    WORKFLOW [optional] Name of the worklow. If provided this command prints a list of docker types available for the workflow.
    """
    content_packages = ctx.obj["content_packages"]
    if package is None:
        _list_content_packages(content_packages)
    elif workflow is None:
        package = _get_package_or_workflow_obj(content_packages, package)
        _list_single_content_package(package)
    else:
        workflow = _get_package_or_workflow_obj(content_packages, package, workflow)
        _list_workflow(workflow)


@cli.command()
@click.pass_context
@click.argument("package")
@click.argument("workflow", required=False, default=None)
def show(ctx, package, workflow):
    """Show details of a package/workflow.

    PACKAGE Name of the content package. This command prints the full description of the package and its license.
    WORKFLOW [optional] Name of the worklow. If provided this command prints details of a workflow.
    """
    content_packages = ctx.obj["content_packages"]
    if workflow is None:
        package = _get_package_or_workflow_obj(content_packages, package)
        try:
            print_content_package(package, compact=False)
        except Exception as err:
            raise click.ClickException(f'Content Package details could not be retrieved:\n{err}')
        else:
            click.echo("\n")
    else:
        workflow = _get_package_or_workflow_obj(content_packages, package, workflow)
        try:
            print_workflow(workflow, compact=False)
        except Exception as err:
            raise click.ClickException(f'Workflow details could not be retrieved:\n{err}')
        else:
            click.echo("\n")


@cli.command()
@click.pass_context
@click.argument("package")
@click.argument("target_dir", type=click.Path(exists=False))
def examples(ctx, package, target_dir):
    """Create local copy of the examples from a package.

    PACAKGE Name of the content package.
    TARGET_DIR Destination folder for copying. The folder must NOT exist.
    """
    content_packages = ctx.obj["content_packages"]
    package = _get_package_or_workflow_obj(content_packages, package)
    if not package.examples:
        raise click.ClickException(
            f"Content package {package.name} does not contain examples."
        )

    target_dir = pathlib.Path(target_dir)
    if target_dir.exists():
        raise click.ClickException(
            f"{target_dir} already exists. Please choose another target directory."
        )

    else:
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package.examples, target_dir)


@cli.command()
@click.pass_context
@click.option(
    "-o",
    "--output-file",
    "target_file",
    type=click.Path(),
    default=None,
    help="output file. If not provided the template will be printed to screen",
)
@click.option(
    "--dry-run", "dry_run", is_flag=True, default=False, help=HELP_STRINGS["dry-run"]
)
@click.option("--package", "-p", "package", default=None, help=HELP_STRINGS["package"])
@click.option(
    "--workflow", "-w", "workflow", default=None, help=HELP_STRINGS["workflow"]
)
@click.argument("workflow_config", type=click.Path(exists=True))
def create_template(ctx, package, workflow, workflow_config, dry_run, target_file):
    """Create template from a workflow config.

    WORKFLOW_CONFIG Path to the workflow config."""
    content_packages = ctx.obj["content_packages"]
    if workflow is None or package is None:
        package, workflow, workflow_config = _get_workflow_from_cfg(workflow_config)
    workflow = _get_package_or_workflow_obj(content_packages, package, workflow)
    try:
        ret = workflow.create_template(
            workflow_config=workflow_config, target_file=target_file, return_cmd=dry_run
        )
    except Exception as err:
        raise click.ClickException('Template creation failed. This is most likely due to an invalid workflow file. '
                                   'Rerun with option `--dry-run` and use the printed command to debug the workflow.')
    if isinstance(ret, list):
        click.echo(" ".join(ret))
    elif isinstance(ret, str):
        click.echo(ret)


@cli.command()
@click.pass_context
@click.option(
    "--dry-run", "dry_run", is_flag=True, default=False, help=HELP_STRINGS["dry-run"]
)
@click.option(
    "--docker-type",
    "-t",
    "docker_type",
    type=str,
    default=None,
    help="select a specific docker type. Run `aicore-content list <contentPacakge> <workflow>` to list available types.",
)
@click.option("--package", "-p", "package", default=None, help=HELP_STRINGS["package"])
@click.option(
    "--workflow", "-w", "workflow", default=None, help=HELP_STRINGS["workflow"]
)
@click.argument("workflow_config", type=click.Path(exists=True))
def create_image(
    ctx,
    package,
    workflow,
    workflow_config,
    dry_run,
    docker_type,
    docker_type_key=".dockerType",
):
    """Create template from a workflow config.

    WORKFLOW_CONFIG Path to the workflow config."""
    content_packages = ctx.obj["content_packages"]
    if workflow is None or package is None:
        package, workflow, workflow_config = _get_workflow_from_cfg(workflow_config)
    else:
        with pathlib.Path(workflow_config).open() as stream:
            workflow_config = yaml.safe_load(stream)
    workflow = _get_package_or_workflow_obj(content_packages, package, workflow)
    docker_type = (
        workflow_config.get(docker_type_key, None)
        if docker_type is None
        else docker_type
    )
    if "image" not in workflow_config:
        raise click.ClickException(
            "Error: the provided workflow config is missing an 'image' entry."
        )
    if docker_type is not None and docker_type not in workflow.dockerfiles.keys():
        raise click.ClickException(
            f"Docker type {docker_type} is not available. Run "
            "`aicore-content show <package> <workflow>` to get a list of docker types available."
        )
    try:
        ret = workflow.create_image(
            workflow_config=workflow_config, docker_type=docker_type, return_cmd=dry_run
        )
    except Exception as err:
        raise click.ClickException('Image creation failed. This is most likely due to an invalid Dockerfile. '
                                   'Rerun with option `--dry-run` and use the printed command to debug the dockerfile.')
    if isinstance(ret, list):
        click.echo(" ".join(ret))
