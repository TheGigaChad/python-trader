import enum
from dataclasses import dataclass, field

from pytrader.common.asset import Asset


class OrderStatus(enum.Enum):
    """
    Status of the request depending on what is happening to it.
    """
    INIT = "init"
    QUEUED = "queued"
    PROCESSING = "processing"
    FILLED = "filled"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class OrderType(enum.Enum):
    """
    Type of order that we want fulfilled.
    """
    BUY = "BUY"
    SELL = "SELL"
    PRICE_TEST_BUY = "PRICE_TEST_BUY"
    PRICE_TEST_SELL = "PRICE_TEST_SELL"


@dataclass
class Order:
    """
        This is a class for mathematical operations on complex numbers.

        Attributes:
            real (int): The real part of complex number.
            imag (int): The imaginary part of complex number.
    """

    __type: OrderType
    __asset: Asset
    __status: OrderStatus = field(init=False, default=OrderStatus.INIT)

    def __repr__(self):
        return f"Order(type: {self.__type}, asset: {self.__asset}, status: {self.__status})"

    def __str__(self):
        return f"Order(type: {self.__type}, asset: {self.__asset}, status: {self.__status})"

    @property
    def type(self) -> OrderType:
        return self.__type

    @property
    def asset(self) -> Asset:
        return self.__asset

    @property
    def status(self) -> OrderStatus:
        return self.__status

    @status.setter
    def status(self, new_status: OrderStatus):
        self.__status = new_status
