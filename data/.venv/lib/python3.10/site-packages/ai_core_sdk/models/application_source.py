from typing import Dict


class ApplicationSource:
    """The ApplicationSource object defines the application source.

        :param repo_url: URL of the repository, defaults to None
        :type repo_url: str, optional
        :param path: path within the repository, defaults to None
        :type path: str, optional
        :param revision: revision number of the application, defaults to None
        :type revision: str, optional
        """

    # pylint:disable=W0613
    def __init__(self, repo_url: str = None, path: str = None, revision: str = None, **kwargs):
        self.repourl: str = repo_url
        self.path: str = path
        self.revision: str = revision

    def __str__(self):
        return "ApplicationSource repourl: " + str(self.repourl) + ", ApplicationSource revision: " + str(self.revision)

    @staticmethod
    def from_dict(application_source_dict: Dict[str, str]):
        """Returns a :class:`ai_core_sdk.models.application_source.ApplicationSource` object, created from the values in
        the dict provided as parameter

        :param application_source_dict: Dict which includes the necessary values to create the object
        :type application_source_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.application_source.ApplicationSource`
        """
        return ApplicationSource(**application_source_dict)
