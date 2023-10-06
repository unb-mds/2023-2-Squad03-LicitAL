from typing import Any, Dict, List

from ai_core_sdk.models.application_source import ApplicationSource
from ai_core_sdk.models.application_resource_sync_status import ApplicationResourceSyncStatus


class ApplicationStatus:
    """The Application object defines the application.

        :param health_status: Application health status, defaults to None
        :type health_status: str, optional
        :param sync_status: Application sync status, defaults to None
        :type sync_status: str, optional
        :param message: Application health status message, defaults to None
        :type message: str, optional
        :param source: Application source, defaults to None
        :type source: class:`ai_core_sdk.models.application_status.ApplicationStatus`, optional
        :param sync_finished_at: Application sync finish time, defaults to None
        :type sync_finished_at: str, optional
        :param sync_started_at: Application sync start time, defaults to None
        :type sync_started_at: str, optional
        :param reconciled_at: Application reconciliation time, defaults to None
        :type reconciled_at: str, optional
        :param sync_ressources_status: Status of the synchronization of the application resources, defaults to None
        :type sync_ressources_status:
            List[class:`ai_core_sdk.models.application_resource_sync_status.ApplicationResourceSyncStatus`], optional
        """

    def __init__(self, health_status: str = None, sync_status: str = None, message: str = None,
                 source: ApplicationSource = None, sync_finished_at: str = None, sync_started_at: str = None,
                 reconciled_at: str = None, sync_ressources_status: List[ApplicationResourceSyncStatus] = None,
                 **kwargs):
        self.health_status: str = health_status
        self.sync_status: str = sync_status
        self.message: str = message
        self.source: ApplicationSource = source
        self.sync_finished_at: str = sync_finished_at
        self.sync_started_at: str = sync_started_at
        self.reconciled_at: str = reconciled_at
        self.sync_ressources_status: List[ApplicationResourceSyncStatus] = sync_ressources_status

    def __str__(self):
        return "ApplicationStatus health status: " + str(self.health_status) + \
               ", ApplicationStatus sync status: " + str(self.sync_status) + \
               ", ApplicationStatus message: " + str(self.message) + ", " + str(self.source)

    @staticmethod
    def from_dict(application_status_dict: Dict[str, Any]):
        """Returns a :class:`ai_core_sdk.models.application_status.ApplicationStatus` object, created from the values in
        the dict provided as parameter

        :param application_status_dict: Dict which includes the necessary values to create the object
        :type application_status_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.application_status.ApplicationStatus`
        """
        if 'source' in application_status_dict:
            application_status_dict['source'] = ApplicationSource.from_dict(application_status_dict['source'])
        if 'sync_ressources_status' in application_status_dict:
            application_status_dict['sync_ressources_status'] = [
                ApplicationResourceSyncStatus.from_dict(asd)
                for asd in application_status_dict['sync_ressources_status']
            ]
        return ApplicationStatus(**application_status_dict)
