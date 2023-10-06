from typing import Any, Dict, List

from ai_core_sdk.models import Label
from ai_core_sdk.models.resource_group_status import ResourceGroupStatus


class ResourceGroup:
    """ResourceGroup represents the resource group.

    :param resource_group_id: The resource_group_id of this ResourceGroup.
    :type resource_group_id: str
    :param tenant_id: The tenant_id of this ResourceGroup.
    :type tenant_id: str
    :param zone_id: The zone_id of this ResourceGroup.
    :type zone_id: str
    :param labels: The labels of this ResourceGroup.
    :type labels: ResourceGroupLabels
    :param status: The status of this ResourceGroup.
    :type status: str
    :param status_message: The status_message of this ResourceGroup.
    :type status_message: str
    """
    def __init__(self, resource_group_id: str = None, tenant_id: str = None, zone_id: str = None,
                 labels: List[Label] = None, status: ResourceGroupStatus = None, status_message: str = None, **kwargs):
        self.resource_group_id: str = resource_group_id
        self.tenant_id: str = tenant_id
        self.zone_id: str = zone_id
        self.labels: List[Label] = labels
        self.status: ResourceGroupStatus = status
        self.status_message: str = status_message

    def __str__(self):
        return "Resource group id: " + str(self.resource_group_id)

    @staticmethod
    def from_dict(resource_group_dict: Dict[str, Any]):
        """Returns a :class:`ai_core_sdk.models.resource_group.ResourceGroup` object, created
        from the values in the dict provided as parameter

        :param resource_group_dict: Dict which includes the necessary values to create the object
        :type resource_group_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.resource_group.ResourceGroup`
        """
        if 'resource_group_status' in resource_group_dict:
            resource_group_dict['resource_group_status'] = \
                ResourceGroupStatus(resource_group_dict['resource_group_status'])
        if 'labels' in resource_group_dict:
            resource_group_dict['labels'] = [Label.from_dict(l) for l in resource_group_dict['labels']]
        return ResourceGroup(**resource_group_dict)
