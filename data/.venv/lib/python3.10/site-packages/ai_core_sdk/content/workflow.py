import ast
import pathlib
import string
import warnings
from abc import ABC, abstractmethod
from asyncio import subprocess
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from subprocess import PIPE, Popen, check_output, run
from typing import Any, Dict, List, Tuple, Union

import yaml


__all__ = ["WorkflowType", "Workflow"]


class WorkflowType(Enum):
    """Different types workflows supported."""

    ExecutionMetaflow = "green"
    # DeploymentGenerator = 'magenta'
    DeploymentYaml = "bright_magenta"


MANDATORY_KEYS = {
    None: ("type",),
    WorkflowType.ExecutionMetaflow: ("py", "className"),
    WorkflowType.DeploymentYaml: ("yaml",),
}


def str_representer(dumper, data):
    """Dumps YAML multi-line strings when necessary"""
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def ensure_workflow_config(workflow_config):
    """Loads a workflow config when needed and validates it"""
    if isinstance(workflow_config, (str, pathlib.Path)):
        with pathlib.Path(workflow_config).open() as stream:
            workflow_config = yaml.safe_load(stream)
    if not isinstance(workflow_config, dict):
        raise AttributeError("workflow_config is mandatory!")
    return workflow_config


@dataclass
class Workflow:
    """The Workflow object representing a workflow.
    Usually instances of this class are not created manually but are created from a
    class:`ai_core_sdk.content.content_package.ContentPackage` instance.
    :param name: Name of the workflow
    :type name: str
    :param path: Path to the workflow file. Type of the file depends on the worklfow type.
    :type path: pathlib.Path
    :param type: Type of the workflow
    :type type: class:`ai_core_sdk.content.workflow.WorkflowType`
    :param content_package_version: Version of the content package
    :type content_package_version: Union[str, None], optional
    :param class_name: Name of the content package's class_name
    :type class_name: Union[str, None], optional
    :param description: Description text
    :type description: str, optional
    :param additional_options: Version str
    :type additional_options: Dict[str, Any], optional
    """

    name: str
    path: pathlib.Path
    type: WorkflowType
    content_package_version: Union[str, None] = None
    class_name: Union[str, None] = None
    dockerfiles: Dict[str, pathlib.Path] = None
    description: str = field(default_factory=str)
    additional_options: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_entry(
        cls,
        name: str,
        entry: Dict[str, Any],
        content_package_version: Union[None, str] = None,
    ) -> "Workflow":
        """Create a worfklow from dictionary.
        Usually instances of this class are not created manually but are created from a
        class:`ai_core_sdk.content.content_package.ContentPackage` instance.
        :param name: Name of the workflow
        :type name: str
        :param entry: Path to the workflow file. Type of the file depends on the worklfow type.
        :type entry: Dict[str, Any]
        :param content_package_version: Version of the content package
        :type content_package_version: Union[str, None], optional
        :raises: class:`KeyError`
        :return: Workflow
        :rtype: class:`ai_core_sdk.content.workflow.Workflow`
        """
        if any([k not in entry.keys() for k in MANDATORY_KEYS[None]]):
            raise KeyError(
                "All workflow definitions require the key(s): "
                + ", ".join(MANDATORY_KEYS[None])
            )
        try:
            template_type = WorkflowType[entry["type"]]
        except KeyError:
            raise KeyError(f"Unkown workflow type '{entry['type']}'")
        if any([k not in entry.keys() for k in MANDATORY_KEYS[template_type]]):
            raise KeyError(
                f"Worfklow definitions of '{template_type.name}' require the key(s): "
                + ", ".join(MANDATORY_KEYS[template_type])
            )
        if template_type == WorkflowType.DeploymentYaml:
            path = entry["yaml"]
            class_name = None
        if template_type == WorkflowType.ExecutionMetaflow:
            path = entry["py"]
            class_name = entry["className"]
        dockerfiles = entry.get("dockerfile", None)
        if isinstance(dockerfiles, str) or isinstance(dockerfiles, pathlib.Path):
            dockerfiles = {"default": pathlib.Path(dockerfiles)}
        if isinstance(dockerfiles, dict):
            dockerfiles = {n: pathlib.Path(p) for n, p in dockerfiles.items()}
        else:
            dockerfiles = {}
        return cls(
            name=name,
            path=pathlib.Path(path),
            content_package_version=content_package_version,
            type=template_type,
            class_name=class_name,
            dockerfiles=dockerfiles,
            description=entry.get("description", ""),
            additional_options=entry.get("additionalOptions", {}),
        )

    def validate(self) -> None:
        """Run validationfor the content package definition and its workflows.
        :raises: class:`ValueError`
        """
        msg = f"Validation of worflow '{self.name}' failed: "
        failed = False
        if not self.path.exists():
            failed = True
            msg += f"\n- Workflow path {self.path} does not exist"
        else:
            if self.type is WorkflowType.ExecutionMetaflow:
                try:
                    self._get_py_class_from_template_file()
                except ValueError:
                    failed = True
                    msg += f"\n- Class '{self.class_name}' not defined in {self.path}"
        for tag, dockerfile in self.dockerfiles.items():
            if not dockerfile.exists():
                failed = True
                msg += f"\n- Dockerfile ({tag}) path {dockerfile} does not exist"
        if failed:
            raise ValueError(msg)

    def raw_metaflow_cli(
        self, *args: str, return_cmd: bool = False
    ) -> Union[str, None]:
        """Execute metaflow CLI command.
        This functions is to execute metaflow CLI commands on a workflow
        python file. The basic structure of the CLI commands is:
        `cd <base folder of the workflow> && python -m<flow.py> *args`.
        :param `*args`: CLI arguments as strings
        :type `*args`: str
        :param return_cmd: Return the command instead of executing it
        :type return_cmd: bool, optional
        :raises: class:`CalledProcessError`
        :return: Command as list of str or None
        :rtype: Union[List[str], None]
        """
        if self.type is not WorkflowType.ExecutionMetaflow:
            raise TypeError("Workflow is ")
        cwd = self.path.parent
        flow = self.path.stem
        cmd = ["python", f"-m{flow}"] + [*args]
        if return_cmd:
            return cmd
        check_output(cmd, cwd=cwd)

    def _dockerfile_path(self, docker_type):
        """
        Find a path of a Dockerfile by its type.
        If the docker_type is None, a 1st Dockerfile found is used.
        """
        if len(self.dockerfiles) == 0:
            raise KeyError(f"No Dockerfile available!")
        if docker_type is None:
            docker_type = [*self.dockerfiles.keys()][0]
        try:
            return pathlib.Path(self.dockerfiles[docker_type])
        except KeyError:
            raise KeyError(f"Unknown docker_type '{docker_type}'")

    def _create_code_package(self):
        """
        Create a code package file in the directory of the flow script.
        Ignore all errors.
        """
        flow = self.path.stem
        cmd = ["python", f"-m{flow}", "package", "save", "codepkg.tgz"]
        run(cmd, cwd=self.path.parent)

    def create_image(
        self,
        workflow_config: Union[str, pathlib.Path, Dict],
        docker_type: Union[None, str] = None,
        return_cmd: bool = False,
        silent: bool = False
    ):
        """Create docker image based on workflow_config.
        The image is created using the tag workflow_config['image'].
        :param workflow_config: Path to the workflow config or dictionary from a loaded workflow config
        :type workflow_config: Union[str, pathlib.Path, Dict]
        :param dockertype: Specific docker type, if not set the first in the dockerfiles definition is being used.
        :type dockertype: str, optional
        :param return_cmd: Return the command instead of executing it
        :type return_cmd: str, optional
        :raises: class:`CalledProcessError`, class:`AttributeError`
        :return: Command as list of str or None
        :rtype: Union[List[str], None]
        """
        workflow_config = ensure_workflow_config(workflow_config)
        pkg_version = self.content_package_version or ''
        docker_file = self._dockerfile_path(docker_type)

        if self.type == WorkflowType.ExecutionMetaflow:
            self._create_code_package()

        cmd = [
            "docker",
            "build",
            "--platform=linux/amd64",
            f"--tag={workflow_config['image']}",
            "--build-arg",
            f"pkg_version={pkg_version}",
            f"-f{docker_file}",
            f"{docker_file.parent}"
        ]
        if return_cmd:
            return cmd
        check_output(cmd, stderr=PIPE if silent else None)

    def _get_py_class_from_template_file(self):
        if self.class_name is None:
            raise ValueError("Attribute class_name is None.")
        with self.absolute_path.open() as fd:
            file_contents = fd.read()
        module = ast.parse(file_contents)
        class_definitions = [
            node for node in module.body if isinstance(node, ast.ClassDef)
        ]
        return class_definitions[
            [c.name for c in class_definitions].index(self.class_name)
        ]

    def _create_template_deployment(self, workflow_config):
        # keep multi-line strings
        yaml.representer.SafeRepresenter.add_representer(str, str_representer)

        with self.path.open() as stream:
            tmpl = defaultdict(dict, yaml.safe_load(stream))
            if "name" in workflow_config:
                tmpl["metadata"]["name"] = workflow_config["name"]
            if "labels" in workflow_config:
                tmpl["metadata"]["labels"] = {**tmpl["metadata"]["labels"], **workflow_config["labels"]}
            if "annotations" in workflow_config:
                tmpl["metadata"]["annotations"] = {**tmpl["metadata"]["annotations"], **workflow_config["annotations"]}

            # use only keys for 'image*' and 'imagePullSecret*' for variables substitution
            cfg = {k: v for k,v in workflow_config.items() if k.startswith('image')}
            spec = string.Template(tmpl["spec"]["template"]["spec"])
            tmpl["spec"]["template"]["spec"] = spec.safe_substitute(cfg)
            return dict(tmpl)

    def _create_template_execution_metaflow_commands(self, workflow_config):
        workflow_config = {**{".workflow-yaml-template-kwargs": self.additional_options}, **workflow_config}
        metaflow_args, argo_args, argo_create_args = generate_metaflow_args_from_workflow_config(workflow_config)
        flow = self.path.stem
        cmd = ["python", "-Wignore", f"-m{flow}"]
        cmd += [*metaflow_args]
        cmd += ["argo"] + argo_args + ["create"]
        cmd += [*argo_create_args]
        cmd += ["--only-json"]
        return cmd

    def _create_template_execution(self, commands, silent):
        output = check_output(commands,
                              stderr=PIPE if silent else None,
                              cwd=self.path.parent)
        return output.decode("utf-8")

    def create_template(
        self,
        workflow_config: Union[str, pathlib.Path, Dict, None],
        target_file: Union[str, pathlib.Path, None] = None,
        return_cmd: bool = False,
        silent: bool = False
    ) -> Union[List[str], None]:
        """Create docker image based on workflow_config.
        The image is created using the tag workflow_config['image'].
        :param workflow_config: Path to the workflow config or dictionary from a loaded workflow
        config.
        :type workflow_config: Union[str, pathlib.Path, Dict, NOne]
        :param target_file: Output path for the template. If None the template will be printed.
        :type target_file: Union[str, pathlib.Path, None], optional
        :param return_cmd: Return the command instead of executing it
        :type return_cmd: str, optional
        :raises: class:`CalledProcessError`, class:`AttributeError`
        :return: Command as list of str or None
        :rtype: Union[List[str], None]
        """
        workflow_config = ensure_workflow_config(workflow_config)

        if self.type == WorkflowType.DeploymentYaml:
            deployment = self._create_template_deployment(workflow_config)
            template = yaml.safe_dump(deployment)
        elif self.type == WorkflowType.ExecutionMetaflow:
            cmds = self._create_template_execution_metaflow_commands(workflow_config)
            if return_cmd:
                return cmds
            template = self._create_template_execution(cmds, silent)
        else:
            raise ValueError(
                f"{self.type} can not be used to create an AICore template."
            )

        if target_file:
            target_file = pathlib.Path(target_file).resolve()
            with target_file.open("w") as stream:
                stream.write(template)
                return None

        return template

    @property
    def absolute_path(self) -> pathlib.Path:
        """Return absolute path of the workflow file (py/yaml).
        :return: Path
        :rtype: class:`pathlib.Path`
        """
        if not self.path.is_absolute():
            raise ValueError("Path of the workflow is not absolute path!")
        return self.path

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Workflow(name='{self.name}', type={self.type.name})"


class WorkflowConfigOps(ABC):
    """Abstract class to define expected entries in a workflow config
    and the CLI args they result in.
    """

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def __call__(self, key: str, value: Any) -> None:
        """Register an entry.
        :param key: Key of the entry.
        :type key: str
        :param value: Value
        :type value: Any
        """
        ...

    @abstractmethod
    def collect(self) -> Tuple[Union[str, List], Union[str, List], Union[str, List]]:
        """Return CLI arguments from the collected entries.
        Calling this function should also set the class to its initial state.
        """
        ...


class CopyPasteOps(WorkflowConfigOps):
    """Workflow config entry to be used directly as CLI argument.
    :param n_args: Number of different cli argument types
    :type n_args: int
    :param pos: Position of the CLI arguments in the return of CopyPasteOps.collect()
    :param pos: int
    """

    def __init__(self, n_args: int, pos: int):
        self.n_args = n_args
        self.pos = pos
        self.values = []

    def __call__(self, _: str, value: Union[List[str], str]) -> None:
        """Register an entry.
        :param _: Key of the workflow config entry (not processed)
        :type _: str
        :param v: Entry as a single str or a list of str
        :type v: Union[List[str], str]
        """
        self.values.extend([value] if isinstance(value, str) else value)

    def collect(self) -> Tuple[List[str]]:
        """Returns n_args Lists of cli arguments.
        :return: Tuple of cli arguments lists.
        :rtype: Tuple[List[str]]
        """
        args = [list() for _ in range(self.n_args)]
        if len(self.values) > 0:
            args[self.pos].extend(self.values)
        self.values = []
        return args


class NamedOps(WorkflowConfigOps):
    """Workflow config entry to be a named options --<name>=<entry>.
    :param n_args: Number of different cli argument types
    :type n_args: int
    :param pos: Position of the CLI arguments in the return of CopyPasteOps.collect()
    :param pos: int
    """

    def __init__(self, key, n_args, pos):
        self.key = key
        self.n_args = n_args
        self.pos = pos
        self.values = []

    def __call__(self, _: str, value: str) -> None:
        """Register an entry.
        :param _: Key of the workflow config entry (not processed)
        :type _: str
        :param value: Entry as a single str or a list of str
        :type value: Union[List[str], str]
        """
        self.values.append(value)

    def collect(self):
        args = [list() for _ in range(self.n_args)]
        if len(self.values) > 0:
            args[self.pos].extend([f"--{self.key}={v}" for v in self.values])
        self.values = []
        return args


class DictOps(WorkflowConfigOps):
    def __init__(self, key, n_args, pos):
        self.key = key
        self.n_args = n_args
        self.pos = pos
        self.entry = {}

    def __call__(self, _, entry):
        self.entry = {**self.entry, **entry}

    def collect(self):
        args = [list() for _ in range(self.n_args)]
        args[self.pos].extend(
            [f'--{self.key}="{k}:{v}"' for k, v in self.entry.items()]
        )
        self.entry = {}
        return args


class KubernetesOps(WorkflowConfigOps):
    def __init__(self):
        self.image = None
        self.secret = None

    def __call__(self, k, v):
        if k in "objectStoreSecret":
            self.secret = v.strip()
        elif k == "image":
            self.image = v.strip()
        else:
            raise ValueError

    def collect(self):
        if self.image is None and self.secret is None:
            return [], [], []
        arg = "--with=kubernetes:"
        opts = ([f"image={self.image}"] if self.image else []) + (
            [f"secrets={self.secret}"] if self.secret else []
        )
        arg += ",".join(opts)
        self.image = self.secret = None
        return arg, [], []


class Template(WorkflowConfigOps):
    def __init__(self, template, n_args):
        self.template = template
        self.n_args = n_args

    def __call__(self, _, v):
        for key, args in v.items():
            if key in self.template.keys():
                self.template[key](key, args)
        return self

    def collect(self):
        args = [list() for _ in range(self.n_args)]
        for key, entry in self.template.items():
            new_args = entry.collect()
            assert len(new_args) == len(args)
            for i in range(len(args)):
                args[i].extend(
                    [new_args[i]] if isinstance(new_args[i], str) else new_args[i]
                )
        return args


def generate_metaflow_args_from_workflow_config(workflow_config: Dict):
    kubernetes_ops = KubernetesOps()

    metaflow_plain_args = CopyPasteOps(3, 0)
    workflow_plain_args = CopyPasteOps(3, 2)
    label_ops = DictOps("label", 3, 2)
    annotation_ops = DictOps("annotation", 3, 2)
    additional_ops = Template(
        {
            "step": metaflow_plain_args,
            "metaflow": metaflow_plain_args,
            "labels": label_ops,
            "annotations": annotation_ops,
            "pipeline": workflow_plain_args,
            "workflow": workflow_plain_args,
        },
        n_args=3,
    )

    special_keywords = {
        ".workflow-yaml-template-kwargs": additional_ops,
        "objectStoreSecret": kubernetes_ops,
        "image": kubernetes_ops,
        "additionalOptions": additional_ops,
        "name": NamedOps("name", 3, 1),
        "labels": label_ops,
        "annotations": annotation_ops,
        "imagePullSecret": NamedOps("image-pull-secret", 3, 2),
    }
    return Template(special_keywords, n_args=3)(None, workflow_config).collect()
