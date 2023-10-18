from multiprocessing.sharedctypes import Value
import pathlib
from typing import Union, Dict, Any, List
from types import ModuleType
import os
import importlib
import pkgutil
from importlib.machinery import SourceFileLoader
import warnings
import uuid
from functools import lru_cache
import inspect

import yaml
from dotenv import load_dotenv

from .workflow import Workflow


__all__ = [
    "ContentPackage",
    "get_content_packages",
    "get_content_packages_from_module",
    "get_content_packages_from_py_file",
]


DEFAULT_REPO_SPEC_FILE = "ai_core_content_spec.py"
ENV_VARIABLE_NAME = "AI_CORE_CONTENT_SPECS"


@lru_cache()
def _get_mandatory_parameters(func, blacklist):
    signature = inspect.signature(func)
    return [
        k
        for k, v in signature.parameters.items()
        if v.default is inspect.Parameter.empty and k not in blacklist
    ]


class ContentPackage:
    """The ContentPackage object defines a content packages
    :param name: Name of the package
    :type name: str
    :param workflows: Dict of workflows see class:`ai_core_sdk.content.workflow.Workflow` for details
    :type workflows: Union[Dict[str, Any], None]
    :param workflows_base_path: Base path for all relative paths in the workflow definition
    :type workflows_base_path: Union[str, pathlib.Path]
    :param examples: Paths to a folder containing examples
    :type examples: Union[str, pathlib.Path, None], optional
    :param license: Name of the content package's license
    :type license: Union[str, None], optional
    :param description: Description text
    :type description: Union[str, None], optional
    :param version: Version str
    :type version: Union[str, None], optional
    """

    _mandatory_keys = ("name", "workflows", "workflows_base_path")

    def __init__(
        self,
        name: str,
        workflows: Union[Dict[str, Any], None],
        workflows_base_path: Union[str, pathlib.Path],
        examples: Union[str, pathlib.Path, None] = None,
        license: Union[str, None] = None,
        description: Union[str, None] = None,
        version: Union[str, None] = None,
    ):
        self.name = name
        self.description = description
        self.version = version
        self.workflows_base_path = pathlib.Path(workflows_base_path).resolve()
        self.license = license
        if examples is not None:
            examples = pathlib.Path(examples).resolve()
        self.examples = examples
        workflows = {} if workflows is None else workflows
        if not isinstance(workflows, dict):
            raise TypeError("'workflows' has to be None or a dictionary.")
        self._workflows_raw = workflows
        self._workflows = None

    @staticmethod
    def check_path(
        path: Union[pathlib.Path, str],
        validate_is_dir: bool = False,
        validate_is_file: bool = False,
    ) -> Union[None, str]:
        """Funciton to check the existence of a path.
        :param path: Path, which is transformed into an absolute path by the function prior to validation
        :type path: Union[str, pathlib.Path]
        :param validate_is_file: Bool specifying whether to check if the file is a folder
        :type path: bool, optional
        :param validate_is_dir: Bool specifying whether to check if the path is a folder
        :type path: bool, optional
        :return: str in case of a valid path and None in case of an invalid path
        :rtype: Union[None, str]
        """
        if path is None:
            return None
        path = pathlib.Path(path).resolve()
        if path.exists():
            if not validate_is_dir and not validate_is_file:
                return str(path)
            elif validate_is_dir and validate_is_file:
                raise ValueError(
                    "The path should be a folder and a file at the same time."
                )
            elif validate_is_file and path.is_file():
                return str(path)
            elif validate_is_dir and path.is_dir():
                return str(path)
        return None

    def validate(self) -> None:
        """Run validationfor the content package definition and its workflows.
        :raises: ValueError when validations fails
        """
        msg = f"Validation of content package '{self.name}' failed: "
        failed = False
        try:
            workflows = self.workflows.values()
        except Exception as err:
            failed = True
            msg += f"\n- Initialization of the workflows failed:\n"
            msg += str(err.args[0])
        else:
            for workflow in self.workflows.values():
                workflow.validate()
        if (
            self.examples is not None
            and self.check_path(self.examples, validate_is_dir=True) is None
        ):
            failed = True
            msg += f"\n- {self.examples} is not a valid file path to an examples dir"
        if failed:
            raise ValueError(msg)

    @property
    def workflows(self) -> Dict[str, Workflow]:
        """Return dict of workflows from the ContentPackage.
        :return: Dict of workflows from the ContentPackage
        :rtype: Dict[str, Workflow]
        """
        if self._workflows is None:
            workflows = {}
            for name, entry in self._workflows_raw.items():
                if not name.startswith(".") and not name.startswith("_"):
                    try:
                        entry = _transform_paths_workflow_entry(
                            self.workflows_base_path, entry
                        )
                        workflow = Workflow.from_entry(name, entry, self.version)
                    except (KeyError, ValueError, TypeError) as err:
                        raise KeyError(
                            f"Invalid workflow definition for '{name}':\n{err.args[0]}"
                        )
                    workflows[workflow.name] = workflow
            self._workflows = workflows
        return self._workflows

    def __getitem__(self, name: str) -> Workflow:
        """Get Workflow by its name.
        :raises: class:`ai_core_sdk.content.workflow.WorkflowNotFound`
        :return: Workflow
        :rtype: class:`ai_core_sdk.content.workflow.Workflow`
        """
        try:
            return self.workflows[name]
        except IndexError:
            raise WorkflowNotFound(self, name)

    @classmethod
    def from_yaml(cls, yaml_path: Union[pathlib.Path, str]) -> "ContentPackage":
        """Initialize a content package from a yaml file.
        :param yaml_path: Path to the yaml file
        :type yaml_path: Union[pathlib.Path, str]
        :raises: class:`FileNotFoundError`, class:`ValueError`
        :return: ContentPackage
        :rtype: class:`ai_core_sdk.content.content_package.ContentPackage`
        """
        mandatory_parameters = _get_mandatory_parameters(cls.__init__, ("self",))
        yaml_path = pathlib.Path(yaml_path).resolve()
        if not yaml_path.exists():
            raise FileNotFoundError(f"Package file {yaml_path} not found!")
        root_path = yaml_path.parent
        with yaml_path.open() as stream:
            spec = yaml.safe_load(stream)
        if not isinstance(spec, dict):
            mandatory_parameters = ", ".join(f"'{p}'" for p in mandatory_parameters)
            raise ValueError(
                f"Invalid yaml file. It has to specifiy a dictionary with the keys: {mandatory_parameters}"
            )
        spec["workflows_base_path"] = root_path
        if any([p not in spec for p in mandatory_parameters]):
            mandatory_parameters = ", ".join(f"'{p}'" for p in mandatory_parameters)
            raise KeyError(
                f"Not all mandatory parameters {mandatory_parameters} specify in {yaml_path}."
            )
        if "examples" in spec.keys():
            spec["examples"] = root_path / spec["examples"]
        return cls(
            name=spec["name"],
            workflows=spec["workflows"],
            workflows_base_path=spec["workflows_base_path"],
            examples=spec.get("examples", None),
            license=spec.get("license", None),
            description=spec.get("description", None),
            version=spec.get("version", None),
        )

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        s = f"ContentPackage(name='{self.name}', '"
        w = ", ".join(["'" + w.name + "'" for w in self.workflows.values()])
        s += f"'workflows=[{w}])"
        return s


class WorkflowNotFound(Exception):
    """Exception thrown in case of invalid workflow query on a ContentPacakge object"""

    def __init__(self, repo: ContentPackage, requested_template: str):
        self.avaible_pipelines_message = "Workflows available are:\n"
        self.avaible_pipelines_message += "\n".join(
            [f"\t- {k}" for k in repo.workflows.keys()]
        )
        self.requested_template = requested_template
        self.message = (
            f"Workflow `{self.requested_template}` not found!\n"
            + self.avaible_pipelines_message
        )
        super().__init__(self.message)


def _transform_paths_workflow_entry(
    base_path: Union[str, pathlib.Path], entry: Dict[str, Any]
) -> Dict[str, Any]:
    """Append the base_path to all relative paths in a workflow entry.
    :param base_path: base path that is appended to all relative paths in the entry dict
    :type base_path: Union[str, pathlib.Path]
    :param entry: Entry dictionary
    :type entry: Dict[str, Any]
    :raises: class:`TypeError`
    :return: Transformed entry dictionary
    :rtype: Dict[str, Any]
    """
    base_path = pathlib.Path(base_path)
    make_absolute = lambda p: p if p.is_absolute() else base_path / p
    if not isinstance(entry, dict):
        raise TypeError("Workflow entry has to be a dict.")
    dockerfile = entry.get("dockerfile", None)
    if isinstance(dockerfile, str) or isinstance(dockerfile, pathlib.Path):
        entry["dockerfile"] = make_absolute(pathlib.Path(dockerfile))
    elif isinstance(dockerfile, dict):
        for name, path in entry["dockerfile"].items():
            entry["dockerfile"][name] = make_absolute(pathlib.Path(path))
    elif dockerfile is None:
        pass
    else:
        raise TypeError(
            f'"dockerfile" entry of type {type(dockerfile)}. Only str and pathlib.Path allowed.'
        )
    py_file = entry.get("py", None)
    if isinstance(py_file, str) or isinstance(py_file, pathlib.Path):
        entry["py"] = make_absolute(pathlib.Path(py_file))
    yaml_file = entry.get("yaml", None)
    if isinstance(yaml_file, str) or isinstance(yaml_file, pathlib.Path):
        entry["yaml"] = make_absolute(pathlib.Path(yaml_file))
    return entry


def _discover_content_packages(
    content_spec_py: str = DEFAULT_REPO_SPEC_FILE,
) -> List[pathlib.Path]:
    """Run discovery for content packages.
    There are two discovery mechanisms: search for python files defining content packages
    in installed packages and through paths set in an environment variable.
    :param content_spec_py: file name to search for in installed packages
    :type content_spec_py: str, optional
    :return: List of content package definition files
    :rtype: List[pathlib.Path]
    """
    content_packages = []
    for i in pkgutil.iter_modules(
        None
    ):  # returns a tuple (path, package_name, ispkg_flag)
        if i.ispkg:
            try:
                content_packages.append(
                    _find_content_spec_file(i.name, content_spec_py)
                )
            except ValueError:
                pass
    load_dotenv(".env")
    try:
        additional_spec_files = [
            pathlib.Path(p.strip()) for p in os.environ[ENV_VARIABLE_NAME].split(":")
        ]
    except KeyError:
        pass
    else:
        content_packages.extend(
            [p for p in additional_spec_files if p.exists() and p.is_file()]
        )
    return [*set(content_packages)]


def get_content_packages_from_module(
    module: Union[str, ModuleType], content_spec_py: str = DEFAULT_REPO_SPEC_FILE
) -> List[ContentPackage]:
    """Search for content package definition within a module.
    :param module: Name of a module as str or imported module
    :type module: Union[str, ModuleType]
    :param content_spec_py: file name to search for in the module
    :type content_spec_py: str, optional
    :return: List of content packages class:`ai_core_sdk.content.content_package.ContentPackage`
    :rtype: List[ContentPackage]
    """
    content_spec = _find_content_spec_file(module, content_spec_py)
    return get_content_packages_from_py_file(content_spec)


def _find_content_spec_file(
    module: Union[str, ModuleType], content_spec_py: str = DEFAULT_REPO_SPEC_FILE
) -> pathlib.Path:
    if isinstance(module, str):
        module_spec = importlib.util.find_spec(module)
        if module_spec is None:
            raise ImportError(f"No module name {module}")
    elif isinstance(module, ModuleType):
        module_spec = module.__spec__
    else:
        raise ValueError("module has either be name of the module or a loaded module")
    locations = module_spec.submodule_search_locations
    content_spec = None
    for loc in locations if locations else []:
        content_spec = pathlib.Path(loc) / content_spec_py
        if content_spec.exists():
            break
        else:
            content_spec = None
    if content_spec is None:
        raise ValueError(
            f"Module {module} does not contain a file named {content_spec_py}"
        )
    return content_spec


def _load_and_check_packages(path: Union[str, pathlib.Path], raise_errors: bool = True):
    path = pathlib.Path(path)
    if path.suffix == ".py":
        pkgs = get_content_packages_from_py_file(path)
    elif path.suffix == ".yaml":
        pkgs = [get_content_package_from_yaml_file(path)]
    else:
        raise ValueError(
            f'"{path.suffix}" is not a valid content package defintion file type.'
        )
    for pkg in pkgs:
        try:
            pkg.validate()
        except Exception as err:
            err_str = "; ".join(err.args) if hasattr(err, "args") else str(err)
            msg = f"Invalid package '{pkg.name}' [{path}]:\n{err_str}"
            raise ValueError(msg)
    return pkgs


def get_content_packages(
    manual_paths: Union[None, List[Union[str, pathlib.Path]]] = None,
    raise_errors: bool = True,
) -> Dict[str, ContentPackage]:
    """Retrieve all content packages available.
    If raising errors is turned off, then warnings are sent instead.
    :param manual_paths: Additional paths to content package definitions
    :type manual_paths: Union[None, List[Union[str, pathlib.Path]]], optional
    :param raise_errors: Raise errors instead of warnings
    :type raise_errors: bool, optional
    :raises: class:`ValueError`
    :return: Dictionary of class:`ai_core_sdk.content.content_package.ContentPackage`
    :rtype: List[ContentPackage]
    """
    paths = _discover_content_packages()
    paths.extend(manual_paths if manual_paths else [])
    paths = [*set([pathlib.Path(p) for p in paths])]

    packages = {}
    packages_paths = {}

    f_err_str = (
        lambda err: "; ".join([str(a) for a in getattr(err, "args", err)])
    )

    pkgs = []
    for path in paths:
        try:
            pkgs.extend(_load_and_check_packages(path))
        except Exception as err:
            if raise_errors:
                raise
            else:
                warnings.warn(f_err_str(err))
    for pkg in pkgs:
        if pkg.name in packages:
            msg = f"Tried to load a package named '{pkg.name}' [{path}] twice."
            msg += f" {packages_paths[pkg.name]} was added previously"
            if raise_errors:
                raise ValueError(msg)
            else:
                warnings.warn(msg)
                continue
        packages[pkg.name] = pkg
        packages_paths[pkg.name] = path
    return packages


def get_content_package_from_yaml_file(
    yaml_file: Union[str, pathlib.Path]
) -> ContentPackage:
    """Load content pacakge from a yaml file.
    If raising errors is turned off, then warnings are sent instead.
    :raises: class:`ValueError`, class:`FileNotFoundError`
    :return: class:`ai_core_sdk.content.content_package.ContentPackage`
    :rtype: class:`ai_core_sdk.content.content_package.ContentPackage`
    """
    yaml_file = pathlib.Path(yaml_file)
    try:
        content_package = ContentPackage.from_yaml(yaml_file)
    except FileNotFoundError as err:
        msg = f"Package file {yaml_file} not found!"
        raise FileNotFoundError(msg)
    except KeyError as err:
        msg = str(err)
        raise ValueError(msg)
    except Exception as err:
        msg = f"Error during loading of package file '{yaml_file}':\n{err}"
        raise ValueError(msg)
    return content_package


def get_content_packages_from_py_file(
    py_file: Union[str, pathlib.Path]
) -> List[ContentPackage]:
    """Load content pacakges from a python file.
    If raising errors is turned off, then warnings are sent instead.
    :raises: class:`ValueError`, class:`FileNotFoundError`
    :return: List of class:`ai_core_sdk.content.content_package.ContentPackage`
    :rtype: List[ContentPackage]
    """
    py_file = pathlib.Path(py_file)
    try:
        module = SourceFileLoader(  # pylint: disable=E1120
            fullname=uuid.uuid4().hex[:6].upper(), path=str(py_file)
        ).load_module()
    except FileNotFoundError as err:
        if not py_file.exists():
            msg = f"Package file {py_file} not found!"
            raise FileNotFoundError(msg)
        else:
            msg = f"Error raised while loading content package from '{py_file}':\n{err}"
            raise ValueError(msg)
    except Exception as err:
        msg = f"Error raised while loading content package from '{py_file}':\n{err}"
        raise ValueError(msg)
    specs = []
    for obj in dir(module):
        if obj.startswith("_"):
            continue
        obj = getattr(module, obj)
        if obj.__class__.__name__ == ContentPackage.__name__:
            kwargs = {**obj.__dict__}
            del kwargs["_workflows"]
            kwargs["workflows"] = kwargs["_workflows_raw"]
            del kwargs["_workflows_raw"]
            obj = ContentPackage(**kwargs)
            specs.append(obj)
    if len(specs) == 0:
        msg = f"No ContentPackage objects found in file {py_file}."
        raise ValueError(msg)
    return specs
