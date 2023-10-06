import ast
import textwrap
import json
from typing import Type
import yaml
import pathlib
import re
from importlib.machinery import SourceFileLoader
import io
from contextlib import redirect_stdout, redirect_stderr
import uuid

import click

from .workflow import WorkflowType


MISSING_DESCRIPTION_MSG = "[No description found]"


def _clean_text(s):
    s = s.replace("\n", " ")
    s = s.replace("\t", " ")
    s = re.sub(" +", " ", s)
    return s


def _format_entry(s, initial_ident="\t- "):
    wrapper = textwrap.TextWrapper(
        initial_indent=initial_ident,
        tabsize=4,
        expand_tabs=True,
        subsequent_indent="\t  ",
    )
    return wrapper.fill(_clean_text(s))


def add_metaflow_parameters_help_to_doc_string(flow: "FlowSpec"):
    """Utility function to append parameters to
    metaflow.FlowSpec doc string.

    Patameter
    ---------
    flow: metaflow.FlowSpec
        The flow of which the DocString should be extended.
    """
    doc_str = []
    for _, par in flow._get_parameters(flow):
        par_str = [par.name, "--------"]
        if "default" in par.kwargs:
            par_str.append(f'default={par.kwargs["default"]}')
        if "type" in par.kwargs:
            try:
                type_str = par.kwargs["type"].__name__
            except AttributeError:
                type_str = str(par.kwargs["type"])
            par_str.append(f"type={type_str}")
        help_str = par.kwargs.get("help", "")
        if len(help_str) > 0:
            help_str = textwrap.indent("\n".join(textwrap.wrap(help_str)), "    ")
        par_str.append(help_str)
        doc_str.append("\n".join(par_str))

    if flow.__doc__ is None:
        flow.__doc__ = "\n\n".join(doc_str)
    else:
        flow.__doc__ += "\n" + "\n\n".join(doc_str)


def get_deployment_yaml_parameters_as_string(template):
    template = pathlib.Path(template)
    if template.suffix == ".yaml":
        with template.open() as stream:
            template = yaml.safe_load(stream)
    elif template.suffix == ".json":
        with template.open() as stream:
            template = json.load(stream)
    template_inputs = template.get("spec", {}).get("inputs", {})
    input_parameters = template_inputs.get("parameters", [])
    input_artifacts = template_inputs.get("artifacts", [])
    doc_str = []
    parameter_str = []
    for par in input_parameters:
        par_str = [par["name"], "--------"]
        parameter_type = par.get("type", None)
        if parameter_type:
            par_str.append(f"type={parameter_type}")
        default_value = par.get("default", None)
        if default_value:
            par_str.append(f"default={default_value}")
        parameter_str.append("\n".join(par_str))
    if len(parameter_str) > 0:
        parameter_str = ["Input Paramters\n========"] + parameter_str
        doc_str.append("\n\n".join(parameter_str))
    artifact_str = []
    for par in input_artifacts:
        par_str = [par["name"], "--------"]
        parameter_type = par.get("type", None)
        if parameter_type:
            par_str.append(f"type={parameter_type}")
        default_value = par.get("default", None)
        if default_value:
            par_str.append(f"default={default_value}")
        artifact_str.append("\n".join(par_str))
    if len(artifact_str) > 0:
        artifact_str = ["Input Artifacts\n========"] + artifact_str
        doc_str.append("\n\n".join(artifact_str))
    return "\n\n".join(doc_str)


def print_content_package(content_pkg, compact=False):
    msg = click.style(f"{content_pkg.name}", fg="red")
    msg += "\n" + "=" * 20 + "\n"
    desc = content_pkg.description if isinstance(content_pkg.description, str) else ""
    if len(desc) > 0:
        desc = _format_entry(desc.split("\n")[0] if compact else desc)
    else:
        desc = _format_entry(MISSING_DESCRIPTION_MSG)
    if not compact and content_pkg.license:
        msg += f"License: {content_pkg.license}\n"
    msg += desc
    click.echo(msg)


def _print_execution_metaflow_workflow(msg, workflow, compact):
    if compact:
        desc = workflow.description if isinstance(workflow.description, str) else ""
        doc_str = ast.get_docstring(workflow._get_py_class_from_template_file())
        desc += "" if doc_str is None or doc_str == 0 else ("\n" + doc_str)
        desc = _format_entry(desc if len(desc) > 0 else MISSING_DESCRIPTION_MSG)
        msg += desc
        click.echo(msg)
    else:
        click.echo(msg)
        from metaflow.cli import cli
        from metaflow import FlowSpec
        workflow.absolute_path
        module = SourceFileLoader( # pylint: disable=E1120
            fullname=uuid.uuid4().hex[:6].upper(), path=str(workflow.absolute_path)
        ).load_module()
        pipeline = getattr(module, workflow.class_name)
        if not issubclass(pipeline, FlowSpec):
            raise TypeError(f'{workflow.class_name} is not metaflow.Flowspec')
        f = cli.commands["show"].callback
        while hasattr(f, "__wrapped__"):
            f = f.__wrapped__
        add_metaflow_parameters_help_to_doc_string(pipeline)

        class GraphProxy:
            graph = pipeline(use_cli=False)._graph

        with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
            f(GraphProxy)
            msg = buf.getvalue()
        click.echo(msg)


def _print_deployment_yaml_workflow(msg, workflow, compact):
    desc = workflow.description if isinstance(workflow.description, str) else ""
    desc = _format_entry(desc if len(desc) > 0 else MISSING_DESCRIPTION_MSG)
    msg += desc
    if not compact:
        msg += "\n\n" + get_deployment_yaml_parameters_as_string(workflow.absolute_path)
    click.echo(msg)


def print_workflow(workflow, compact=True):
    msg = click.style(f"{workflow.name} [{workflow.type.name}]", fg=workflow.type.value)
    msg += "\n" + "=" * 20 + "\n"
    if workflow.type == WorkflowType.ExecutionMetaflow:
        _print_execution_metaflow_workflow(msg, workflow, compact)
    elif workflow.type == WorkflowType.DeploymentYaml:
        _print_deployment_yaml_workflow(msg, workflow, compact)
    else:
        raise ValueError(f'Workflows of type {workflow.type} can not be printed.')
