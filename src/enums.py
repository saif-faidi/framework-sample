from enum import Enum, auto


class ExitCode(Enum):
    SUCCESS = 0
    GENERAL_ERROR = 1
    INVALID_ARGUMENTS = 2
    PERMISSION_DENIED = 13
    FILE_NOT_FOUND = 127


class FileExtension(Enum):
    TXT = auto()
    CSV = auto()
    JSON = auto()
    XML = auto()
    YAML = auto()
    # You can add more file extensions as needed
