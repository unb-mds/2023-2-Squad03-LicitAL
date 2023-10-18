# AICore Content Packages

The `ai_core_sdk.content` module should help to build and deliver content packages for SAP AI Core.

The main functionalities are:
-

## Package Consumption


### 1. Install AI Core SDK**

Install the `ai-core-sdk` with content package support.

```
pip install ai-core-sdk[aicore-content]
```

This also installs the command `aicore-content`

### 2. Install/Retrieve Content

Content packages are availble right after python module installation when they contain a `ai_core_content_spec.py`. See [Package Creation](#package-creation) for more details.

Alternativly e.g. for local custom content package the path to the `ai_core_content_spec.py` has to be added to the environment variable `AI_CORE_CONTENT_SPECS` or provided explicitly to the `aicore-content` using `-c <path to content spec py/yaml>`

### 3. Discover Content Packages and their Content

**CLI**

Echo descriptions of all packages from all registires:
```
aicore-content list
```

To add custom content package spec the environment variable `AI_CORE_CONTENT_SPECS` ([`.env`](https://pypi.org/project/python-dotenv/) file is also supported ) or the `-c <path to content spec py/yaml>` option can be used:
```
aicore-content -c ai_core_content_spec.py list
export AI_CORE_CONTENT_SPECS=$PWD/ai_core_content_spec.py && aicore-content show
echo "AI_CORE_CONTENT_SPECS=$PWD/ai_core_content_spec.py" >> .env && aicore-content show
```

**Python**

All packages:
```python
from ai_core_sdk.content import get_content_packages # function to fetch a list of all packages from all registries

for content_pkg in get_content_packages().values():
    content_pkg.print() # print more details for each package
```

The content specs can also be used directly:
```python
from content_package.ai_core_content_spec import package_spec_obj
package_spec_obj.print()
```


A content packages consistens of multiple *workflows*. *Workflows* can be AI Core *Executions* or *Deployments*.

**CLI**

List of all workflows available:
```
aicore-content list <name of the package>
```

Details of a specific workflow:
```
aicore-content show <name of the package> <name of the workflow>
```

**Python**

All packages:

```python
from ai_core_sdk.content import get_content_packages # function to fetch a list of all packages from all registries

package = [*get_content_packages().values()][0] # Get a ContentPackage object
workflows = package.workflows # get all workflows from a package
for flow in workflows:
    flow.print(compact=True) # Print a compact description of the workflow
for flow in workflows:
    flow.print(compact=False) # Print a detailed description of the workflow.
```

When using `python` a package can also directly used from the `ContentPackage` file without registering:

```python
# Load the object from the submodule
from content_package.ai_core_content_spec import package_spec_obj
[*package_spec_obj.workflows.values()][0].print(compact=True)

# create the object from content package spec yaml
from ai_core_sdk.content import ContentPackage

package_spec_obj = ContentPackage.from_yaml('<path to package spec yaml>')
[*package_spec_obj.workflows.values()][0].print(compact=True)

# load content package specs from .py file
from ai_core_sdk.content import get_content_packages_from_py_file
list_of_package_specs = get_content_packages_from_py_file('<path to package spec py>') # a .py file can contain multiple package specs
for package_spec_obj in list_of_package_specs:
    [*package_spec_obj.workflows.values()][0].print(compact=True)
```

### 4. Create Docker Containers and AI Core Templates

To run an execution or start a deployment a template and at least one docker containers are needed. Both components can be generated through the CLI/Python calls. Both ways run a `docker build` internally.

For docker image and template creation some user specific information is needed. This information is provided through a yaml-file called *workflow config*.

A typical config looks like this:
```
.contentPackage: sap-cv
.workflow: batch_processing
.dockerType: gpu
name: "my-executable-name"
label:
  scenarios.ai.sap.com/id: "my-scenario-id"
  ai.sap.com/version: "0.0.1"
annotation:
  scenarios.ai.sap.com/name: "my-scenario-name"
  executables.ai.sap.com/description: "This is a very useful execution pipeline"
  executables.ai.sap.com/name: "idk-what-this-name-is"
image: "my-very-own-docker.repo/sap-cv-batch-processing:0.0.1"
imagePullSecret: "my-docker-registry-secret"
objectStoreSecret: "default-object-store-secret"
```

In this workflow config the target content package and workflow can be referenced using the keys `.package` and `.workflow`. If provided those references are used to create the image and template. If not provided the package and the workflow have to specified thorugh the `--package` and `--workflow` options (see following sections for details).

#### 4.1 Docker Containers

**CLI**

To create the docker containers the CLI has the `aicore-content create-image [--package=<package name>] [--workflow=<workflow name>] <workflow config>` command. The options `--package` and `--workflow` can be omitted when the package and workflow are specifed in the worfklow config. The `create.image` commands runs `docker build` in the background. The image url specified in the workflow config (key `image`) is as the tag for the docker build command. The resulting call can be echoed using the `--dry-run` option:

```
$ aicore_content create-image --package=sap-cv --workflow=batch_processing my-custom-workflow-config.yaml --dry-run
> docker build -t my-very-own-docker.repo/sap-cv-batch-processing:0.0.1 --build-arg pkg_version===1.0.36 -f/Users/I545048/Projects/cv_metaflow_aif/sap-cv-clean-clone/sap_computer_vision/pipelines/batch_pipelines/DockerfileGPU /Users/I545048/Projects/cv_metaflow_aif/sap-cv-clean-clone/sap_computer_vision/pipelines/batch_pipelines
```
Without the `--dry-run` options the building process is started right away:
```
$ aicore_content create-image --package=sap-cv --workflow=batch_processing my-custom-workflow-config.yaml
> Building Dockerfile: /Users/I545048/Projects/cv_metaflow_aif/sap-cv-clean-clone/sap_computer_vision/pipelines/batch_pipelines/DockerfileGPU
> ====================
>
> [+] Building 0.7s (3/14)
> ...
```

The building process has to be followed by a `docker push -t <tag of the container/image specified in workflow config>` to push the container to the registry.

**Python**

The workflow objects got a function `.create_image(...)`:
```python
workflow = content_package_spec_obj['batch_processing'] # fetch the workflow object using its name
docker_tag = 'my-very-own-docker.repo/sap-cv-batch-processing:0.0.1'
workflow_config = 'my-config.yaml'
with open(workflow_config) as stream
    workflow_config = yaml.load(stream)
cmd = workflow.create_image(workflow_config, return_cmd=True) # perform a dry run and return the cmd
print(cmd)
workflow.create_image(workflow_config) # actually build the docker container
os.system(f'docker push {workflow_config["image"]}') # push the container
```

#### 4.2 AICore Templates

The template creation is different for execution and deployment templates.

##### Execution Templates

To create execution templates the [metaflow argo plugin](https://pypi.org/project/sap-ai-core-metaflow/) is used. The CLI and python functions run the metaflow CLI command `python -m <flow py> argo create --only-json` internally.

**CLI**

Execution templates need a workflow config to be provided to the `create-template` subcommand. The options `--package` and `--workflow` can be omitted when the package and workflow are specifed in the worfklow config.
```
aicore-content create-image [--package=<package name>] [--workflow=<workflow name>] <workflow config> -o <path to output template.json>
```

This commands creates a AI Core template file that can used be after used in AI Core:
```
cd my-onboarded-git-repo
aicore-content my-package template my-workflow my-template-config.yaml -o aicore-template.json
git add aicore-template.json
git commit -m "add content package template"
git push
```
All additonal options

**Python**

The workflow config for execution templates has to be provided to the workflows's `.create_template(...)` function. The output file can be specified through the keyword parameter `target_file`:
```python
workflow_config_path = 'my-template-config.yaml'
output_json = 'aicore-template.json'
workflow.create_template(workflow_config_path, target_file=output_json)
```

**Additonal Options**

Additional arguments can be defined in the workflow config under the key `additionalOptions`. There are 4 types of additional options:
- `workflow`: List of CLI arguments as strs. Those additonal arguments are passed to the CLI call as arguments for the workflow
- `metaflow`: List of CLI arguments as strs. Those additonal arguments are passed to the CLI call as arguments for metaflow
```yaml
...
additonal-options:
    workflow: # list of strings passed as workflow options
        ...
    metaflow: # list of strings passed as metaflow options
        - --package-suffixes=.py,.sh
```
Strings in the `workflow`/`metaflow` pasted into these positions:
```
python -m flow [metaflow] argo create [workflow]
```

To check the resulting call an `--dry-run`(CLI)/`return_cmd=True`(Python) option is availble. Alternativly the subcommand `aicore-content <package name> metaflow-cli <workflow name>` or `workflow.raw_metaflow_cli(...)`. Every input after the command is directly passed to the underlying `python -m <flow>` call.

##### Deployment Templates

There is currently no template generator for deployments. Therefore, currently `template` command/`create_template(...)` function only copies a template yaml to the target file. All tenant specific values have to be edited by hand.


## Package Creation

A content package needs two additional files: the `ContentPackage` file and a workflows yaml.

### `ContentPackage`

Content package are defined in a `ContentPackage` instance. This instance can either be loaded from a `.py`file or can be created from a yaml. A typical `.py` file looks like this:
```python
import pathlib
import yaml
from ai_core_sdk.content import ContentPackage

HERE = pathlib.Path(__file__).parent

workflow_yaml = HERE / 'workflows.yaml'
with workflow_yaml.open() as stream:
    workflows = yaml.safe_load(stream)

spec = ContentPackage(
    name='my-package name', # name of the package and the aicore-content cli subcommand
    workflows_base_path=workflow_yaml.parent, # Base paths for all relative paths in the workflow dict
    workflows=workflows,
    description='This is an epic content package.', # Package description
    examples=HERE / 'examples', # Folder to package related examples [optional]
    version='0.0.1' # Version of the package
)
```
If the package is to be distributed as a python module via Nexus or PyPI and the content package spec python file should be included in the package as `ai_core_content_spec.py`. This allows the CLI to find the package without additional configuration efforts and creates a subcommand using the name from the `ContentPackage.name` attribute.

#### Examples

Examples for the content package can copy by the consumer to a directory using the command `aicore-content examples <package name> <target folder>`. This command creates the target folder and copies all files from the paths set in the `ContentPackage`. If no path is set or the path does not exists the `examples` subcommand is not created.

#### Version

Currently the version in the `ContentPackage` is passed to the docker build call as  `--build-arg pkg_version==={version}`. In the `Dockerfile` this build argument can be used to build the docker container using the local version of the package. This is useful for content packages distributed as module through Nexus or PyPI:
```Dockerfile
FROM pytorch/pytorch
ARG pkg_version=
ENV pkg_version=$pkg_version
...
RUN python -m pip install sap-computer-vision-package${pkg_version}
```

### Workflows File

The second mandatory file a workflows yaml. This yaml is used to define workflows and is structed like a dictionary:
Entries of the dict look like this:
```Yaml
name-of-the-workflow:
    description: >
        Description text [optional]
    dockerfile: ...
    type: ExecutionMetaflow/DeploymentYAML
    [... more type specific fields]
```
It is important that all paths in the workflow yaml are specified as paths relative to the workflow yaml`s path. This also means that all files must be located in the same folder or in subfolders.

### Dockerfiles

The dockerfile entry can either be a single:
```Yaml
dockerfile: train_workflow/Dockerfile
```
or a dictionary of paths:
```Yaml
dockerfile:
    cpu: train_workflow/Dockerfile
    gpu: train_workflow/Dockerfile
```
This allows to define different Docker container for different node types or multiple containers for cases where different steps use different containers. The different dockerfile can be selected using the option/argument `docker_type` when running the build docker command/function.

### Types

Currently two types of workflows are supported:
- `ExecutionMetaflow`: exections defined as metaflow flowspecs
- `DeploymentYaml`: deployment defined as yamls

#### ExecutionMetaflow

Additional fields for a `ExecutionMetaflow` entry are
- `py`: path to the python file containing the `metaflow.FlowSpec` class
- `className`: name of the `metaflow.FlowSpec` class
- `additionalOptions` (optional): The section is identical to the `additionalOptions` from the workflow configs.

```Yaml
train-workflow:
    description: >
        Description text [optional]
    dockerfile:
        cpu: train/Dockerfile
        cpu: train/DockerfileGPU
    type: ExecutionMetaflow
    py: train/flow.py
    className: TrainingFlow
    additonal-options:
        annotations:
            artifacts.ai.sap.com/datain.kind: dataset
            artifacts.ai.sap.com/trainedmodel.kind: model
        labels:
            ...
        workflow: # list of strings passed as workflow options
            ...
        metaflow: # list of strings passed as metaflow options (only valid for ExecutionMetaflow)
            - --package-suffixes=.py,.sh
```

#### `ContentPackage` from yaml

The specification of a content package and of the workflows can also be merged into a single yaml file:
```yaml
name: test-spec-yaml
examples: examples
description: |
  this is a test.
show_files:
  test: SHOW_FILE
workflows:
  test_execution:
    type: ExecutionMetaflow
    className: TestPipeline
    py: train/flow.py
    dockerfile:
      cpu: train/Dockerfile
      gpu: train/DockerfileGPU
    annotations:
      artifacts.ai.sap.com/datain.kind: dataset
      artifacts.ai.sap.com/trainedmodel.kind: model
    metaflow:
      - --package-suffixes=.py,.s
```

Currently there is no discovery mechanism for yaml specs.

They either have to be consumed in python:
```python
from ai_core_sdk.content import ContentPackage
content_package = ContentPackage.from_yaml(spec_yaml)
```

or made available to the CLI through the `aicore-content -c <path to the spec yaml> ...` option or through the `AI_CORE_CONTENT_SPECS` environment variable.

