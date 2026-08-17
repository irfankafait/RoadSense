from enum import Enum


class SortOrder(str, Enum):
    """
    Defines the supported accident sorting directions.
    """

    ASC = "asc"
    DESC = "desc"