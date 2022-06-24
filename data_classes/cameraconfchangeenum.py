# Personal Project
__author__ = "Eolus"

# Standard libraries
from enum import IntEnum, unique
# Third party libraries
# Custom libraries


@unique
class CameraConfChangeEnum(IntEnum):
    NEW = 1
    MODIFIED = 2
    DELETED = 3
