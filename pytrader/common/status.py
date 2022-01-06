import enum


class Status(enum.Enum):
    """
    enum corresponding to the status of the manager
    """
    UNKNOWN   = 0
    IDLE      = 1
    STARTING  = 2
    RUNNING   = 3
    ERROR     = 4
    STOPPED   = 5
    SCHEDULED = 6

