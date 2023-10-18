from typing import Any, Dict, List, Union


class Kpi:
    """The Kpi object defines the Kpi data.
    """

    def __init__(self, header: List[str], rows: List[Union[str, int]], **kwargs):
        self.header: List[str] = header
        self.rows: List[Union[str, int]] = rows

    def __str__(self):
        return "KPIs header(s): " + ', '.join(self.header)

    @staticmethod
    def from_dict(kpi_dict: Dict[str, Any]):
        """Returns a :class:`ai_core_sdk.models.kpi.Kpi` object, created
        from the values in the dict provided as parameter

        :param kpi_dict: Dict which includes the necessary values to create the object
        :type kpi_dict: Dict[str, Any]
        :return: An object, created from the values provided
        :rtype: class:`ai_core_sdk.models.kpi.Kpi`
        """
        return Kpi(**kpi_dict)
