import sys
import re


def convert_input_paths(argo_json):
    """
    argo aggregation is not valid json as properties are not enclosed in quotes:
    flow/step/[{task-id:flow-step-3119439657},{task-id:flow-step-195521861}]

    Parameters
    ----------
    argo_json

    Returns
    -------
    list of task-ids to be consumed by metaflow join step:
    flow/step/:flow-step-3119439657,flow-step-195521861
    """
    flow, run_id, task_ids = argo_json.split("/")
    task_ids = re.sub(r"[\[\]{}]", "", task_ids)
    task_ids = task_ids.split(",")
    tasks = [t.split(":")[1] for t in task_ids]
    return "{}/{}/:{}".format(flow, run_id, ",".join(tasks))


if __name__ == "__main__":
    print(convert_input_paths(sys.argv[1]))
