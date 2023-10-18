from typing import Dict


class ApplicationResourceSyncStatus:
    """The ApplicationSyncResourcesStatus object defines the status of sync of application resource.

    :param name: Name of the application resource, defaults to None
    :type name: str, optional
    :param kind: kind of the application resource
    :type kind: str, optional
    :param status: status of the sync of the application resource
    :type status: str, optional
    :param message: application resource message
    :type message: str, optional
    """

    def __init__(self, name: str = None, kind: str = None, status: str = None, message: str = None, **kwargs):
        self.name: str = name
        self.kind: str = kind
        self.status: str = status
        self.message: str = message

    @staticmethod
    def from_dict(app_res_sync_status_dict: Dict[str, str]):
        """Returns a :class:`ai_core_sdk.models.application_resource_sync_status.ApplicationResourceSyncStatus`
        object, created from the values in the dict provided as parameter

        :param app_res_sync_status_dict: Dict which includes the necessary values to create the object
        :type app_res_sync_status_dict: Dict[str, str]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.application_resource_sync_status.ApplicationResourceSyncStatus`
        """
        return ApplicationResourceSyncStatus(**app_res_sync_status_dict)

