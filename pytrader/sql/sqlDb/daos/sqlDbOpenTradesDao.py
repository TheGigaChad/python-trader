import datetime

from pytrader import common


class SQLDbOpenTradesDao:
    """
    dao  that handles the data types from the sql response.
    """

    def __init__(self, name: str, asset_type: common.AssetType, order_type: common.OrderType,
                 trade_intent: common.TradeIntent, qty: float, order_id: int, last_updated: datetime.datetime):
        self.__name: str = name
        self.__order_type: common.OrderType = order_type
        self.__asset_type: common.AssetType = asset_type
        self.__trade_intent: common.TradeIntent = trade_intent
        self.__order_quantity: float = qty
        self.__order_id: int = order_id
        self.__timestamp: datetime.datetime = last_updated

    @property
    def name(self):
        return self.__name

    @property
    def trade_intent(self):
        return self.__trade_intent

    @property
    def quantity(self):
        return self.__order_quantity

    @property
    def order_id(self):
        return self.__order_id

    @property
    def order_type(self):
        return self.__order_type

    @property
    def asset_type(self):
        return self.__asset_type

    @property
    def timestamp(self):
        return self.__timestamp
