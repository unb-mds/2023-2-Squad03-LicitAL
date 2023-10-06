from typing import Dict


class Application:
    """The Application object defines the application.

    :param path: path within the repository
    :type path: str
    :param revision: revision
    :type revision: str
    :param repository_url: URL of the repository
    :type repository_url: str
    :param application_name: name of the application
    :type application_name: str
    """

    # pylint:disable=W0613
    def __init__(self, path: str, revision: str, repository_url: str, application_name: str, **kwargs):
        self.path: str = path
        self.revision: str = revision
        self.repository_url: str = repository_url
        self.application_name: str = application_name

    def __str__(self):
        return "Application name: " + str(self.application_name)

    @staticmethod
    def from_dict(application_dict: Dict[str, str]):
        """Returns a :class:`ai_core_sdk.models.application.Application` object, created from the values in
        the dict provided as parameter

        :param application_dict: Dict which includes the necessary values to create the object
        :type application_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.application.Application`
        """
        return Application(**application_dict)
