from enum import Enum


class ResourceGroupStatus(Enum):
    """ResourceGroupStatus is an Enum defining the valid values of the status of a resource group
    """
    ERROR = 'ERROR'
    PROVISIONED = 'PROVISIONED'
    PROVISIONING = 'PROVISIONING'
