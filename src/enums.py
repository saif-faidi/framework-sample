from enum import Enum, auto


class ExitCode(Enum):
    SUCCESS = 0
    GENERAL_ERROR = 1
    INVALID_ARGUMENTS = 2
    PERMISSION_DENIED = 13
    FILE_NOT_FOUND = 127


