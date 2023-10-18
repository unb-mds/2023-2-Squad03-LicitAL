from enum import Enum


class Status(Enum):
    """Status is an Enum defining the valid values of the status of an execution/deployment
    """
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    DEAD = 'DEAD'
    STOPPING = 'STOPPING'
    STOPPED = 'STOPPED'
    UNKNOWN = 'UNKNOWN'


class ScheduleStatus(Enum):
    """Enum defining the status values for execution schedules
    """
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
