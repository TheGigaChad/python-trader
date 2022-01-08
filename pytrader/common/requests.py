import enum

from pytrader.common.asset import Asset


class RequestType(enum.Enum):
    """
    enum for classifying the type of request made to the exchange.
    """
    UNDEFINED = 0
    INFO = 1
    UPDATE = 2
    BUY = 3
    SELL = 4
    HOLDINGS = 5


class RequestStatus(enum.Enum):
    """
    Status of the request depending on what is happening to it.
    """
    INIT       = 0
    QUEUED     = 1
    PROCESSING = 2
    FILLED     = 3
    FAILED     = 4
    CANCELLED  = 5


class Request:
    """
    Contains the information used to translate what the Trade Manager wants to do to the Exchange Manager.
    """
    def __init__(self, asset: Asset):
        self.__asset: Asset = asset
        self.__instruction = None
        self.__status: RequestStatus = RequestStatus.INIT

