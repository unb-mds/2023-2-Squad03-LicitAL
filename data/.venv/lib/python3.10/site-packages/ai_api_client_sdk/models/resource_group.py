from datetime import datetime
from typing import Any, Dict, List

from .label import Label
from .resource_group_status import ResourceGroupStatus
from ai_api_client_sdk.helpers.datetime_parser import parse_datetime


class ResourceGroup:
    """ResourceGroup represents the resource group.

    :param resource_group_id: The resource_group_id of this ResourceGroup.
    :type resource_group_id: str
    :param labels: The labels of this ResourceGroup.
    :type labels: ResourceGroupLabels
    :param status: The status of this ResourceGroup.
    :type status: str
    :param created_at: Time when the resource group was created
    :type created_at: datetime
    """
    def __init__(self, resource_group_id: str = None, labels: List[Label] = None, status: ResourceGroupStatus = None,
                 created_at: datetime = None, *args, **kwargs):
        self.resource_group_id: str = resource_group_id
        self.labels: List[Label] = labels
        self.status: ResourceGroupStatus = status
        self.created_at: datetime = created_at

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
        if 'created_at' in resource_group_dict:
            resource_group_dict['created_at'] = parse_datetime(resource_group_dict['created_at'])
        return ResourceGroup(**resource_group_dict)
