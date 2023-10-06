from enum import Enum


class RepositoryStatus(Enum):
    """RepositoryStatus is an Enum defining the valid values of the status of a repository
    """
    ERROR = 'ERROR'
    IN_PROGRESS = 'IN-PROGRESS'
    COMPLETED = 'COMPLETED'
