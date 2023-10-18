from typing import Any, Dict


class ObjectStoreSecret:
    """The ObjectStoreSecret object defines the object store secret response.
    """

    def __init__(self, name: str, metadata: Dict[str, str], **kwargs):
        key_prefix = 'storage.ai.sap.com/'
        path_prefix_key = f'{key_prefix}path_prefix'
        self.name: str = name
        self.metadata: Dict[str, str] = metadata
        # pathPrefix key is getting converted into snake case during object mapping d
        # The below code converts path prefix from snake case to camel case
        if path_prefix_key in metadata:
            self.metadata[f'{key_prefix}pathPrefix'] = metadata[path_prefix_key]
            del metadata[path_prefix_key]

    def __str__(self):
        return "Object store secret name: " + str(self.name)

    @staticmethod
    def from_dict(object_store_secret_dict: Dict[str, Any]):
        """Returns a :class:`ai_core_sdk.models.object_store_secret.ObjectStoreSecret` object, created
        from the values in the dict provided as parameter

        :param object_store_secret_dict: Dict which includes the necessary values to create the object
        :type object_store_secret_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.object_store_secret.ObjectStoreSecret`
        """
        return ObjectStoreSecret(**object_store_secret_dict)
