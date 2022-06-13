import datetime

from pytrader.common.asset import AssetType
from pytrader.common.requests import RequestType


class SQLDbTradesDao:
    """
    dao  that handles the data types from the sql response.
    """

    def __init__(self, name: str, order_type: RequestType, quantity: float, order_id: int, timestamp: datetime.datetime,
                 asset_type: AssetType):
        self.__name: str = name
        self.__order_type: RequestType = order_type
        self.__quantity: float = quantity
        self.__order_id: int = order_id
        self.__timestamp: datetime.datetime = timestamp
        self.__asset_type: AssetType = asset_type

    @property
    def name(self):
        return self.__name

    @property
    def order_type(self):
        return self.__order_type

    @property
    def quantity(self):
        return self.__quantity

    @property
    def order_id(self):
        return self.__order_id

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def asset_type(self):
        return self.__asset_type
