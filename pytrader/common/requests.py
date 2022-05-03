import enum

class ResponseType(enum.Enum):
    """
    Response types from the Exchange request
    """
    UNKNOWN       = "UNKNOWN"
    SUCCESSFUL    = "SUCCESSFUL"
    UNSUCCESSFUL  = "UNSUCCESSFUL"
    MARKET_CLOSED = "MARKET_CLOSED"
    EXISTS        = "EXISTS"


class RequestType(enum.Enum):
    """
    enum for classifying the type of request made to the exchange.
    """
    UNDEFINED = "UNDEFINED"
    INFO      = "INFO"
    UPDATE    = "UPDATE"
    BUY       = "BUY"
    SELL      = "SELL"
    HOLDINGS  = "HOLDINGS"

