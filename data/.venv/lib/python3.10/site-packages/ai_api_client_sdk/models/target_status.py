from enum import Enum


class TargetStatus(Enum):
    """TargetStatus is an Enum defining the valid values of the target status of an execution/deployment
    """
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    STOPPED = 'STOPPED'
    DELETED = 'DELETED'
