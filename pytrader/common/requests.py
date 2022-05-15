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
    # TODO - remove BUY/SELL as it is confusing with the Order Type.  We should use Trade instead.
    UNDEFINED = "UNDEFINED"
    INFO = "INFO"
    UPDATE = "UPDATE"
    BUY = "BUY"
    SELL = "SELL"
    HOLDINGS = "HOLDINGS"
    TRADE = "TRADE"
    ALLOWANCE = "ALLOWANCE"
    STATUS = "STATUS"


class ResponseType(enum.Enum):
    """
    enum for classifying the type of request made to the exchange.
    """
    # TODO - remove BUY/SELL as it is confusing with the Order Type.  We should use Trade instead.
    UNDEFINED = "UNDEFINED"
    INFO = "INFO"
    UPDATE = "UPDATE"
    BUY = "BUY"
    SELL = "SELL"
    HOLDINGS = "HOLDINGS"
    TRADE = "TRADE"
    ALLOWANCE = "ALLOWANCE"
    STATUS = "STATUS"
