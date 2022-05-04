import enum

from pytrader.common.asset import Asset


class OrderStatus(enum.Enum):
    """
    Status of the request depending on what is happening to it.
    """
    INIT = 0
    QUEUED = 1
    PROCESSING = 2
    FILLED = 3
    FAILED = 4
    CANCELLED = 5


class OrderType(enum.Enum):
    """
    Type of order that we want fulfilled.
    """
    BUY = "BUY"
    SELL = "SELL"
    PRICE_TEST_BUY = "PRICE_TEST_BUY"
    PRICE_TEST_SELL = "PRICE_TEST_SELL"


class Order:
    """
    contains the data that gets passed to the request call.
    """

    def __init__(self, order_type: OrderType, asset: Asset, qty: float):
        self.__type: OrderType = order_type
        self.__asset: Asset = asset
        self.__status: OrderStatus = OrderStatus.INIT
        self.__qty: float = qty

    @property
    def status(self) -> OrderStatus:
        return self.__status

    @status.setter
    def status(self, new_status: OrderStatus):
        self.__status = new_status

    @property
    def type(self) -> OrderType:
        return self.__type

    @property
    def asset(self) -> Asset:
        return self.__asset

    @property
    def qty(self) -> float:
        return self.__qty
