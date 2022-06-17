import enum


class ResponseStatus(enum.Enum):
    """
    Response types from the Exchange request
    """
    NONE = "NONE"
    UNKNOWN = "UNKNOWN"
    SUCCESSFUL = "SUCCESSFUL"
    UNSUCCESSFUL = "UNSUCCESSFUL"
    MARKET_CLOSED = "MARKET_CLOSED"
    EXISTS = "EXISTS"
    DENIED = "DENIED"


class RequestType(enum.Enum):
    """
    enum for classifying the type of request made to the exchange.
    """
    UNDEFINED = "UNDEFINED"
    INFO = "INFO"
    UPDATE = "UPDATE"
    HOLDINGS = "HOLDINGS"
    TRADE = "TRADE"
    ALLOWANCE = "ALLOWANCE"
    STATUS = "STATUS"
    BUY_SELL_THRESHOLDS = "BUY_SELL_THRESHOLDS"


class ResponseType(enum.Enum):
    """
    enum for classifying the type of request made to the exchange.
    """
    UNDEFINED = "UNDEFINED"
    INFO = "INFO"
    UPDATE = "UPDATE"
    HOLDINGS = "HOLDINGS"
    TRADE = "TRADE"
    ALLOWANCE = "ALLOWANCE"
    STATUS = "STATUS"
    BUY_SELL_THRESHOLDS = "BUY_SELL_THRESHOLDS"
