import json
import os
import shlex
import sys
import posixpath

from metaflow.exception import MetaflowException
from metaflow.metaflow_config import DATASTORE_SYSROOT_S3
from metaflow.metaflow_config import (
    DEFAULT_METADATA,
    SERVICE_INTERNAL_URL,
    SERVICE_HEADERS,
)
from metaflow.parameters import deploy_time_eval
from metaflow.plugins.resources_decorator import ResourcesDecorator
from metaflow.plugins.retry_decorator import RetryDecorator
from metaflow.plugins.catch_decorator import CatchDecorator
from metaflow.plugins.kubernetes.kubernetes_decorator import KubernetesDecorator
from metaflow.plugins.environment_decorator import EnvironmentDecorator
from metaflow.plugins.timeout_decorator import get_run_time_limit_for_task
from metaflow.util import get_username, compress_list
from metaflow.mflog import (
    export_mflog_env_vars,
    bash_capture_logs,
    BASH_SAVE_LOGS,
)
from .argo_client import ArgoClient, ArgoException
from .argo_decorator import ArgoStepDecorator, ArgoInternalStepDecorator

ENTRYPOINT = "entry"
TASK_ID = "{{pod.name}}"
ARGO_API_VERSION = "argoproj.io/v1alpha1"


def dns_name(name):
    """
    Most k8s resource types require a name to be used as
    DNS subdomain name as defined in RFC 1123.
    Hence template names couldn't have '_' (underscore).
    """
    return name.replace("_", "-").lower()


class ArgoWorkflow:
    def __init__(
        self,
        name,
        flow,
        graph,
        code_package,
        code_package_url,
        metadata,
        datastore,
        environment,
        event_logger,
        monitor,
        image_pull_secrets,
        labels,
        annotations,
        volume_claim,
        max_workers,
        workflow_timeout,
    ):
        self.name = name
        self.flow = flow
        self.graph = graph
        self.code_package = code_package
        self.code_package_url = code_package_url
        self.metadata = metadata
        self.datastore = datastore
        self.environment = environment
        self.event_logger = event_logger
        self.monitor = monitor
        self.attributes = {
            "labels": {
                "app": "metaflow",
                "metaflow/workflow_template": name,
                "app.kubernetes.io/created-by": get_username(),
            },
            "annotations": {
                "metaflow/flow_name": flow.name,
            },
        }
        self.system_tags = {
            "metaflow/%s"
            % sys_tag[: sys_tag.index(":")]: dns_name(
                sys_tag[sys_tag.index(":") + 1 :]
            )
            for sys_tag in self.metadata.sticky_sys_tags
        }
        wftmpl = self._compile(
            parse_param_dict(labels),
            parse_param_dict(annotations),
            volume_claim,
            image_pull_secrets,
            max_workers,
            workflow_timeout,
        )
        self._workflow = remove_empty_elements(wftmpl)

    def to_json(self):
        return json.dumps(self._workflow, indent=4)

    def trigger_explanation(self):
        if self._schedule():
            return (
                "This workflow triggers automatically via CronWorkflow *%s*."
                % self.name
            )
        return "No triggers defined. You need to launch this workflow manually."

    def deploy(self, k8s_namespace):
        try:
            ArgoClient(k8s_namespace).create_wf(
                self.name, self._workflow, "workflowtemplates"
            )
        except Exception as e:
            raise ArgoException(str(e)) from e

    def schedule(self, k8s_namespace):
        try:
            client = ArgoClient(k8s_namespace)
            cron = self._schedule()
            if cron is None:
                client.delete_wf(self.name, "cronworkflows")
            else:
                cron_wf = {
                    "apiVersion": ARGO_API_VERSION,
                    "kind": "CronWorkflow",
                    "metadata": {"name": self.name},
                    "spec": {
                        "schedule": cron,
                        "workflowSpec": {"workflowTemplateRef": {"name": self.name}},
                    },
                }
                client.create_wf(self.name, cron_wf, "cronworkflows")
        except Exception as e:
            raise ArgoException(str(e)) from e

    @classmethod
    def trigger(cls, k8s_namespace, name, parameters):
        workflow = {
            "apiVersion": ARGO_API_VERSION,
            "kind": "Workflow",
            "metadata": {"generateName": name + "-"},
            "spec": {
                "arguments": {
                    "parameters": [
                        {"name": n, "value": json.dumps(v)}
                        for n, v in parameters.items()
                    ]
                },
                "workflowTemplateRef": {"name": name},
            },
        }
        try:
            client = ArgoClient(k8s_namespace)
            template = client.get_template(name)
        except Exception as e:
            raise ArgoException(str(e)) from e
        if template is None:
            raise ArgoException(
                "The WorkflowTemplate *%s* doesn't exist on "
                "Argo Workflows. Please deploy your flow first." % name
            )
        try:
            return client.submit(workflow)
        except Exception as e:
            raise ArgoException(str(e)) from e

    @classmethod
    def list(cls, k8s_namespace, name, phases):
        try:
            client = ArgoClient(k8s_namespace)
            tmpl = client.get_template(name)
        except Exception as e:
            raise ArgoException(str(e)) from e
        if tmpl is None:
            raise ArgoException(
                "The WorkflowTemplate *%s* doesn't exist " "on Argo Workflows." % name
            )
        try:
            return client.list_workflows(name, phases)

        except Exception as e:
            raise ArgoException(str(e)) from e

    def _compile(
        self,
        labels,
        annotations,
        volume_claim,
        image_pull_secrets,
        max_workers,
        workflow_timeout,
    ):
        self.parameters = self._parameters()
        return {
            "apiVersion": ARGO_API_VERSION,
            "kind": "WorkflowTemplate",
            "metadata": {
                "name": self.name,
                "labels": {
                    **self.system_tags,
                    **labels,
                    **self.attributes["labels"],
                },
                "annotations": {
                    **annotations,
                    **self.attributes["annotations"],
                },
            },
            "spec": {
                "entrypoint": ENTRYPOINT,
                "workflowMetadata": self.attributes,
                "activeDeadlineSeconds": workflow_timeout,
                "arguments": {
                    "parameters": self.parameters,
                },
                "volumeClaimTemplates": [self._volume_claim_template(volume_claim)],
                "imagePullSecrets": [{"name": sec} for sec in image_pull_secrets],
                "parallelism": max_workers,
                "templates": self._generate_templates(),
            },
        }

    def _schedule(self):
        schedule = self.flow._flow_decorators.get("schedule")
        if schedule:
            # Argo's CRON expression doesn't support 6th field "Year" like AWS EventBridge
            return " ".join(schedule.schedule.split()[:5])
        return None

    def _parameters(self):
        parameters = []
        for _, param in self.flow._get_parameters():
            # Throw an exception if a schedule is set for a flow with required
            # parameters with no defaults.
            is_required = param.kwargs.get("required", False)
            if (
                "default" not in param.kwargs
                and is_required
                and self._schedule() is not None
            ):
                raise MetaflowException(
                    "The parameter *%s* does not have a "
                    "default and is required. Scheduling "
                    "such parameters via Argo CronWorkflow "
                    "is not currently supported." % param.name
                )
            p = {"name": param.name}
            if "default" in param.kwargs:
                v = deploy_time_eval(param.kwargs.get("default"))
                p["value"] = json.dumps(v)
            parameters.append(p)
        return parameters

    def _volume_claim_template(self, storage):
        for node in self.graph.nodes:
            argo_decorator = parse_step_decorator(self.graph[node], ArgoStepDecorator)
            if argo_decorator.get("mount_pvc"):
                template = {
                    "metadata": {"name": self.name + "-pvc"},
                    "spec": {
                        "accessModes": ["ReadWriteOnce"],
                        "resources": {"requests": {"storage": str(storage) + "Mi"}},
                    },
                }
                return template
        return {}

    def _generate_templates(self):
        tasks, nested_dags = self._visit(self.graph["start"], tasks=[], nested_dags=[])
        dag = {"name": ENTRYPOINT, "dag": {"tasks": tasks}}
        container_templates = [
            self.container_template(self.graph[node]) for node in self.graph.nodes
        ]
        return [dag] + nested_dags + container_templates

    def _visit(self, node, tasks, nested_dags, exit_node=None):
        """
        Traverse graph nodes.
        Special treatment of split and foreach subgraphs
        """

        def _linear_or_first_dag_task(node):
            if self._is_foreach_first_child(node):
                return dag_first_task(node)
            if node.name == "start":
                return start_task()
            return linear_task(node)

        if node.type == "end":
            tasks.append(linear_task(node))

        elif node == exit_node:
            pass  # end recursion

        elif node.type in ("start", "linear", "join"):
            tasks.append(_linear_or_first_dag_task(node))
            tasks, nested_dags = self._visit(
                self.graph[node.out_funcs[0]], tasks, nested_dags, exit_node
            )

        elif node.type == "split":
            tasks.append(_linear_or_first_dag_task(node))
            join = self.graph[node.matching_join]
            # traverse branches
            for out in node.out_funcs:
                tasks, nested_dags = self._visit(
                    self.graph[out], tasks, nested_dags, exit_node=join
                )
            # finally continue with join node
            tasks, nested_dags = self._visit(join, tasks, nested_dags, exit_node)

        elif node.type == "foreach":
            tasks.append(_linear_or_first_dag_task(node))
            for_each = foreach_task(node)
            tasks.append(for_each)
            join = self.graph[node.matching_join]
            # create nested dag and add tasks for foreach block
            nested_tasks, nested_dags = self._visit(
                self.graph[node.out_funcs[0]],
                tasks=[],
                nested_dags=nested_dags,
                exit_node=join,
            )
            nested_dags.append(nested_dag(for_each["name"], nested_tasks))
            # join ends the foreach block
            tasks.append(join_foreach_task(join, parent_task=for_each))
            # continue with node after join
            tasks, nested_dags = self._visit(
                self.graph[join.out_funcs[0]], tasks, nested_dags, exit_node
            )

        else:
            raise MetaflowException(
                "Unknown node type: {} in step: {}".format(node.type, node.name)
            )

        return tasks, nested_dags

    def _commands(self, node, retry_count, user_code_retries):
        mflog_expr = export_mflog_env_vars(
            datastore_type="s3",
            stdout_path=posixpath.join("/", "tmp", "mflog_stdout"),
            stderr_path=posixpath.join("/", "tmp", "mflog_stderr"),
            flow_name=self.flow.name,
            run_id="{{workflow.name}}",
            step_name=node.name,
            task_id=TASK_ID,
            retry_count=retry_count,
        )
        init_expr = ""
        if self.code_package_url:
            init_cmds = self.environment.get_package_commands(self.code_package_url, self.datastore.TYPE)
            init_expr = " && ".join(init_cmds)
        step_expr = bash_capture_logs(
            " && ".join(
                self.environment.bootstrap_commands(node.name, self.datastore.TYPE)
                + self._step_commands(node, retry_count, user_code_retries)
            )
        )
        cmd = ["true", mflog_expr, init_expr, step_expr]
        cmd_str = "%s; c=$?; %s; exit $c" % (
            " && ".join(c for c in cmd if c),
            BASH_SAVE_LOGS,
        )
        return shlex.split('bash -c "%s"' % cmd_str)

    def _step_commands(self, node, retry_count, user_code_retries):
        cmds = []
        script_name = os.path.basename(sys.argv[0])
        executable = self.environment.executable(node.name)
        entrypoint = [executable, script_name]

        run_id = "{{workflow.name}}"
        paths = "{{inputs.parameters.input-paths}}"

        if node.name == "start":
            # We need a separate unique ID for the special _parameters task
            task_id_params = "%s-params" % TASK_ID

            params = entrypoint + [
                "--quiet",
                "--metadata=%s" % self.metadata.TYPE,
                "--environment=%s" % self.environment.TYPE,
                "--datastore=%s" % self.datastore.TYPE,
                "--event-logger=%s" % self.event_logger.TYPE,
                "--monitor=%s" % self.monitor.TYPE,
                "--no-pylint",
                "init",
                "--run-id %s" % run_id,
                "--task-id %s" % task_id_params,
            ]
            params.extend(
                [
                    "--%s={{workflow.parameters.%s}}" % (p["name"], p["name"])
                    for p in self.parameters
                ]
            )
            cmds.append(" ".join(params))
            paths = "%s/_parameters/%s" % (run_id, task_id_params)

        if node.type == "join" and self.graph[node.split_parents[-1]].type == "foreach":
            module = "metaflow_extensions.sap.plugins.argowf.argo_convert_aggregation"
            paths = "$(python -m %s %s)" % (module, paths)

        top_level = [
            "--quiet",
            "--metadata=%s" % self.metadata.TYPE,
            "--environment=%s" % self.environment.TYPE,
            "--datastore=%s" % self.datastore.TYPE,
            "--datastore-root=%s" % self.datastore.datastore_root,
            "--event-logger=%s" % self.event_logger.TYPE,
            "--monitor=%s" % self.monitor.TYPE,
            "--no-pylint",
            "--with=argo_internal",
        ]

        step = [
            "step",
            node.name,
            "--run-id %s" % run_id,
            "--task-id %s" % TASK_ID,
            "--retry-count %s" % retry_count,
            "--max-user-code-retries %s" % str(user_code_retries),
            "--input-paths %s" % paths,
        ]

        if any(self.graph[n].type == "foreach" for n in node.in_funcs):
            step.append("--split-index {{inputs.parameters.split-index}}")

        cmds.append(" ".join(entrypoint + top_level + step))
        return cmds

    def _is_foreach_first_child(self, node):
        return node.is_inside_foreach and self.graph[node.in_funcs[0]].type == "foreach"

    def container_template(self, node):
        """
        Returns an argo container template spec. to execute a step
        """
        argo_decorator = parse_step_decorator(node, ArgoStepDecorator)
        env_decorator = parse_step_decorator(node, EnvironmentDecorator)
        retry_decorator = parse_step_decorator(node, RetryDecorator)
        catch_decorator = parse_step_decorator(node, CatchDecorator)
        res_decorator = parse_step_decorator(node, ResourcesDecorator)
        k8s_decorator = parse_step_decorator(node, KubernetesDecorator)
        image = k8s_decorator["image"]
        res = _resources(res_decorator, k8s_decorator)
        env, env_from = _prepare_environment(env_decorator, k8s_decorator)
        volume_mounts = [
            _shared_memory(res_decorator, argo_decorator),
            _pvc_mount(self.name, argo_decorator),
        ]
        user_code_retries = retry_decorator.get("times", 0)
        total_retries = user_code_retries + 1 if catch_decorator else user_code_retries
        retry_count = "{{retries}}" if total_retries else "0"
        cmd = self._commands(node, retry_count, user_code_retries)

        metadata = {
            "labels": {
                **self.system_tags,
                **self.attributes["labels"],
                "metaflow/step_name": dns_name(node.name),
                "app.kubernetes.io/name": "metaflow-task",
                "app.kubernetes.io/part-of": "metaflow",
                "app.kubernetes.io/created-by": get_username(),
                **{
                    k: dns_name(v)
                    for k, v in argo_decorator.get("labels", {}).items()
                },
            },
            "annotations": {
                **self.attributes["annotations"],
                "metaflow/attempt": retry_count,
            },
        }

        template = {
            "name": dns_name(node.name),
            "metadata": metadata,
            "activeDeadlineSeconds": get_run_time_limit_for_task(node.decorators),
            "inputs": {
                "parameters": [{"name": "input-paths"}],
                "artifacts": argo_decorator.get("input_artifacts"),
            },
            "outputs": {
                "parameters": [{"name": "task-id", "value": TASK_ID}],
                "artifacts": argo_decorator.get("output_artifacts"),
            },
            "volumes": [_get_volume(node)],
            "container": {
                "image": image,
                "volumeMounts": volume_mounts,
                "command": [cmd[0]],
                "args": cmd[1:],
                "env": env,
                "envFrom": env_from,
                "resources": {"requests": res, "limits": res},
            },
        }

        if total_retries:
            template["retryStrategy"] = {
                "retryPolicy": "Always",
                # fallback_step for @catch is only executed if retry_count > user_code_retries
                "limit": str(total_retries),
                "backoff": {
                    "duration": "%sm"
                    % str(
                        retry_decorator["minutes_between_retries"]
                        if user_code_retries
                        else 0
                    ),
                },
            }

        if self._is_foreach_first_child(node):
            template["inputs"]["parameters"].append({"name": "split-index"})

        if node.type == "foreach":
            template["outputs"]["parameters"].append(
                {
                    "name": "num-splits",
                    "valueFrom": {"path": ArgoInternalStepDecorator.splits_file_path},
                }
            )

        return template


def _resources(res_decorator, k8s_decorator):
    res = {}
    cpu = res_decorator.get("cpu")
    if cpu:
        res["cpu"] = int(cpu)
    mem = res_decorator.get("memory")
    if mem:
        # argo cluster treats memory as kb
        res["memory"] = str(mem) + "Mi"
    gpu = res_decorator.get("gpu")
    if gpu:
        res["nvidia.com/gpu"] = int(gpu)
    disk = k8s_decorator.get("disk")
    if disk:
        res["ephemeral-storage"] = str(disk) + "Mi"
    return res


def _get_volume(node):
    for deco in node.decorators:
        if isinstance(
            deco, (ResourcesDecorator, ArgoStepDecorator)
        ) and deco.attributes.get("shared_memory"):
            # rely on default linux kernel behaviour to allocate half of available RAM
            # because of this, there is no need to check for the max value
            return {"name": "dev-shm", "emptyDir": {"medium": "Memory"}}
    return {}


def _shared_memory(argo_decorator, resource_decorator):
    for deco in (argo_decorator, resource_decorator):
        shm = deco.get("shared_memory")
        if shm:
            return {"mountPath": posixpath.join("/", "dev", "shm"), "name": "dev-shm"}

    return {}


def _pvc_mount(flow_name, argo_decorator):
    mount_path = argo_decorator.get("mount_pvc")
    if mount_path:
        return {"mountPath": mount_path, "name": flow_name + "-pvc"}

    return {}


def _prepare_environment(env_decorator, k8s_decorator):
    env = {
        "METAFLOW_USER": get_username(),
        "METAFLOW_DATASTORE_SYSROOT_S3": DATASTORE_SYSROOT_S3,
    }
    if DEFAULT_METADATA:
        env["METAFLOW_DEFAULT_METADATA"] = DEFAULT_METADATA
    if SERVICE_INTERNAL_URL:
        env["METAFLOW_SERVICE_URL"] = SERVICE_INTERNAL_URL
    if SERVICE_HEADERS:
        env["METADATA_SERVICE_HEADERS"] = json.dumps(SERVICE_HEADERS)
    # add env vars from @environment decorator if exist
    env.update(env_decorator.get("vars", {}))
    env = [{"name": k, "value": v} for k, v in env.items()]
    env_from = []
    secrets = k8s_decorator.get("secrets")
    if secrets:
        if isinstance(secrets, str):
            secrets = secrets.split(",")
        env_from = [{"secretRef": {"name": s}} for s in secrets]
    return env, env_from


def parse_step_decorator(node, deco_type):
    deco = [d for d in node.decorators if isinstance(d, deco_type)]
    return deco[0].attributes if deco else {}


def start_task():
    return {
        "name": "start",
        "template": "start",
        "arguments": {
            "parameters": [
                {"name": "input-paths", "value": "{{workflow.name}}/_parameters/0"}
            ]
        },
    }


def dag_first_task(node):
    name = dns_name(node.name)
    return {
        "name": name,
        "template": name,
        "arguments": {
            "parameters": [
                {"name": "input-paths", "value": "{{inputs.parameters.input-paths}}"},
                {"name": "split-index", "value": "{{inputs.parameters.split-index}}"},
            ]
        },
    }


def foreach_task(node):
    """
    The inner steps of foreach are encapsulated in a separate template (dag)
    """
    name = dns_name(
        "%s-foreach-%s" % (node.name, node.foreach_param)
    )  # displayed in argo graph
    parent_name = dns_name(node.name)
    return {
        "name": name,
        "template": name,
        "dependencies": [parent_name],
        "arguments": {
            "parameters": [
                {
                    "name": "input-paths",
                    "value": "{{workflow.name}}/%s/{{tasks.%s.outputs.parameters.task-id}}"
                    % (node.name, parent_name),
                },
                {"name": "split-index", "value": "{{item}}"},
            ]
        },
        "withParam": "{{tasks.%s.outputs.parameters.num-splits}}" % parent_name,
    }


def join_foreach_task(node, parent_task):
    name = dns_name(node.name)
    parent_step = node.in_funcs[-1]
    parent_task_name = parent_task["name"]
    return {
        "name": name,
        "template": name,
        "dependencies": [parent_task_name],
        "arguments": {
            "parameters": [
                {
                    "name": "input-paths",
                    "value": "{{workflow.name}}/%s/{{tasks.%s.outputs.parameters}}"
                    % (parent_step, parent_task_name),
                }
            ]
        },
    }


def linear_task(node):
    name = dns_name(node.name)
    paths = [
        "{{workflow.name}}/%s/{{tasks.%s.outputs.parameters.task-id}}"
        % (n, dns_name(n))
        for n in node.in_funcs
    ]
    return {
        "name": name,
        "template": name,
        "dependencies": [dns_name(n) for n in node.in_funcs],
        "arguments": {
            "parameters": [{"name": "input-paths", "value": compress_list(paths)}]
        },
    }


def nested_dag(name, tasks):
    return {
        "name": dns_name(name),
        "inputs": {"parameters": [{"name": "input-paths"}, {"name": "split-index"}]},
        "outputs": {
            "parameters": [
                {
                    "name": "task-id",
                    "valueFrom": {
                        "parameter": "{{tasks.%s.outputs.parameters.task-id}}"
                        % dns_name(tasks[-1]["name"])
                    },
                }
            ]
        },
        "dag": {"tasks": tasks},
    }


def remove_empty_elements(spec):
    """
    Removes empty elements from the dictionary and all sub-dictionaries.
    """
    whitelist = ["none"]  # Don't eliminate artifact's {"archive": {"none": {}}}
    if isinstance(spec, dict):
        kids = {
            k: remove_empty_elements(v) for k, v in spec.items() if v or k in whitelist
        }
        return {k: v for k, v in kids.items() if v or k in whitelist}
    if isinstance(spec, list):
        elems = [remove_empty_elements(v) for v in spec]
        return [v for v in elems if v]
    return spec


def parse_param_dict(param):
    """
    Parses parameters in a form "key:value".
    Removes starting and trailing {}"'.
    """
    if param:
        return dict(
            map(lambda x: x.strip().strip("{}\"'"), a.split(":")) for a in param
        )
    return {}
