class AIAPILimitsEnactments:
    """The AIAPILimitsEnactments object represents the the limits for enactments (common for both executions
    and deployments)

    :param max_running_count: max number of enactments per resource group, <0 means unlimited, defaults to -1
    :type max_running_count: int, optional
    :param `**kwargs`: The keyword arguments are there in case there are additional attributes returned from server
    """
    def __init__(self, max_running_count: int = -1, **kwargs):
        self.max_running_count: int = max_running_count

    def __eq__(self, other):
        if not isinstance(other, AIAPILimitsEnactments):
            return False
        for k in self.__dict__.keys():
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    def __str__(self):
        return str(self.__dict__)
