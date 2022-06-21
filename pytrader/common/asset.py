import datetime
import enum

from pytrader.common.tradeIntent import TradeIntent


class AssetType(enum.Enum):
    """
     Enum used to identify the type of the asset. \n
     """
    UNKNOWN = "UNKNOWN"
    STOCK = "STOCK"
    CRYPTO = "CRYPTO"
    FUND = "FUND"
    PAPER_STOCK = "PAPER_STOCK"
    PAPER_CRYPTO = "PAPER_CRYPTO"


class Asset:
    """
    Class that holds relative data
    """

    def __init__(self, name: str, asset_type: AssetType):
        self.__name: str = name
        self.__type: AssetType = asset_type
        self.__qty: float = 0.0
        self.__value: float = 0.0
        self.__trade_intent: TradeIntent = TradeIntent.UNKNOWN
        self.__last_updated: datetime.datetime = datetime.datetime.now()
        self.__id: int = 0

    def __repr__(self):
        return f"Asset(name: {self.__name}, type: {self.__type}, qty: {self.__qty}, value: {self.__value}, " \
               f"hold_type: {self.__trade_intent}, last_updated: {self.__last_updated}, id: {self.__id})"

    @property
    def qty(self) -> float:
        return self.__qty

    @qty.setter
    def qty(self, q):
        self.__qty = q

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> AssetType:
        return self.__type

    @property
    def trade_intent(self):
        return self.__trade_intent

    @trade_intent.setter
    def trade_intent(self, intent: TradeIntent):
        self.__trade_intent = intent

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, v):
        self.__id = v

    @property
    def last_updated(self) -> datetime.datetime:
        return self.__last_updated

    @last_updated.setter
    def last_updated(self, val: datetime.datetime):
        self.__last_updated = val
