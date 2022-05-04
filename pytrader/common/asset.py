import datetime
import enum
import json
from typing import Optional


class AssetType(enum.Enum):
    """
     Enum used to identify the type of the asset. \n
     """
    UNKNOWN = 0
    STOCK = 1
    CRYPTO = 2
    FUND = 3
    PAPER_STOCK = 4
    PAPER_CRYPTO = 5


class Asset:
    """
    Class that holds relative data
    """

    def __init__(self, name: str, asset_type: AssetType):
        self.__name: str = name
        self.__type: AssetType = asset_type
        self.__holdings = None
        self.__value = None
        self.__hold_type = None
        self.__last_updated: datetime.datetime = datetime.datetime.min

    @property
    def holdings(self) -> float:
        return self.__holdings

    @property
    def value(self) -> float:
        return self.__value

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> AssetType:
        return self.__type

    @property
    def last_updated(self) -> datetime.datetime:
        return self.__last_updated

    @last_updated.setter
    def last_updated(self, val: datetime.datetime):
        self.__last_updated = val
