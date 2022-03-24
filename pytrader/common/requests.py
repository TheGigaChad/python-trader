import enum

from pytrader.common.asset import Asset


class ResponseType(enum.Enum):
    """
    Response types from the Exchange request
    """
    UNKNOWN = "UNKNOWN"
    SUCCESSFUL = "SUCCESSFUL"
    UNSUCCESSFUL = "UNSUCCESSFUL"
    MARKET_CLOSED = "MARKET_CLOSED"


class RequestType(enum.Enum):
    """
    enum for classifying the type of request made to the exchange.
    """
    UNDEFINED = "UNDEFINED"
    INFO = "INFO"
    UPDATE = "UPDATE"
    BUY = "BUY"
    SELL = "SELL"
    HOLDINGS = "HOLDINGS"


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

