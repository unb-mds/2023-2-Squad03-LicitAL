import json
import posixpath

from metaflow.decorators import StepDecorator


class ArgoStepDecorator(StepDecorator):
    """
    Step decorator for Argo Workflows
    ```
    @argo(
        input_artifacts = [
            {
                "name": "test",
                "path": "/tmp"
            }
        ],
        output_artifacts = [
            {
                "name": "test",
                "globalName": "test",
                "path": "/tmp/abc",
                "archive": {"none": {}}
            }
        ],
        labels = [
            {"ai.sap.com/resourcePlan": "train.l"}
        ]
    )
    @step
    def myStep(self):
        ...
    ```
    Parameters
    ----------
    input_artifacts: list
        Argo input artifacts list.
    output_artifacts: list
        Argo outputs artifacts list.
    labels: dict
        Labels to be attached to the step's container.
    mount_pvc: str
        The mount-path for the PersistentVolumeClaim.
    shared_memory: int
        The value for the size (in MiB) of the /dev/shm volume for this step.
    """

    name = "argo"
    defaults = {
        "input_artifacts": [],
        "output_artifacts": [],
        "labels": {},
        "mount_pvc": None,
        "shared_memory": None,
    }


class ArgoInternalStepDecorator(StepDecorator):
    name = "argo_internal"
    splits_file_path = posixpath.join("/", "tmp", "num_splits")

    def task_finished(
        self, step_name, flow, graph, is_task_ok, retry_count, max_user_code_retries
    ):

        if not is_task_ok:
            # The task finished with an exception - execution won't
            # continue so no need to do anything here.
            return

        # For foreaches, we need to export the cardinality of the fan-out
        # into a file that can be read by Argo Workflows output parameter
        # and this be consumable in the next step
        if graph[step_name].type == "foreach":
            self._save_foreach_cardinality(flow._foreach_num_splits)

    def _save_foreach_cardinality(self, num_splits):
        with open(self.splits_file_path, "w") as file:
            json.dump(list(range(num_splits)), file)
