import enum


class Position(enum.Enum):
    """
    The position of the stock relative to our portfolio.
    """
    UNKNOWN = 0
    OWNED = 1
    UNOWNED = 2
    TRADING = 3