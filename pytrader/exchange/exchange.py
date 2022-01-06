import enum
import json
from typing import Optional

from pytrader.common.asset import Asset

from pytrader.config import ALPACA_PAPER_ADDRESS, ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET


class ExchangeName(enum.Enum):
    """
     Enum used to identify the relevant exchange. \n
     """
    UNKNOWN = 0
    ALPACA_PAPER = 1

    def toString(self):
        if self.name == self.UNKNOWN:
            return "UNKNOWN"
        elif self.name == self.ALPACA_PAPER:
            return "ALPACA_PAPER"


class ExchangeType(enum.Enum):
    """
     Enum used to identify the relevant exchange type relating to what it can handle. \n
     """
    UNKNOWN = 0
    PAPER_STOCK = 1
    PAPER_CRYPTO = 2
    STOCK = 3
    CRYPTO = 4


class ExchangeRequestType(enum.Enum):
    """
    enum for classifying the type of request made to the exchange.
    """
    UNDEFINED = -1
    INFO = 0
    UPDATE = 1
    BUY = 2
    SELL = 3


class ExchangeRequestResponseType(enum.Enum):
    """
    Response types from the Exchange request
    """
    UNKNOWN = 0
    SUCCESSFUL = 1
    UNSUCCESSFUL = 2


class ExchangeRequestResponse(enum.Enum):
    """
    Response from the exchange relating to the request.  This contains a status and optional data
    """

    def __init__(self, status: ExchangeRequestResponseType, data: Optional[json] = None):
        self.status = status
        self.data = data


class Exchange:
    """
    Class that holds the exchange type and name in order to classify what it can trade.
    """

    def __init__(self, name: ExchangeName, exchange_type: ExchangeType):
        self.__name: ExchangeName = name
        self.__type: ExchangeType = exchange_type
        self.__url: str = self.__getURL()
        self.__key: str = self.__getKey()
        self.__secret: str = self.__getSecret()
        self.__cash: float = self.__getCash()
        self.__holdings: list[Asset] = []

    def __getURL(self):
        if self.__name == ExchangeName.ALPACA_PAPER:
            return ALPACA_PAPER_ADDRESS

    def __getKey(self):
        if self.__name == ExchangeName.ALPACA_PAPER:
            return ALPACA_PAPER_KEY

    def __getSecret(self):
        if self.__name == ExchangeName.ALPACA_PAPER:
            return ALPACA_PAPER_SECRET

    def __getCash(self):
        return 0.0

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def cash(self):
        cash_params = "cash_pls"
        self.__cash = self.request(request_type=ExchangeRequestType.INFO, request_params=cash_params)
        return self.__cash

    @property
    def holdings(self) -> list[Asset]:
        return self.__holdings

    def request(self, request_type: ExchangeRequestType, request_params: Optional[json] = None):
        if request_type == ExchangeRequestType.UPDATE:
            # TODO - exchange logic
            return ExchangeRequestResponse(status=ExchangeRequestResponseType.SUCCESSFUL)
        elif request_type == ExchangeRequestType.INFO:
            return ExchangeRequestResponse(status=ExchangeRequestResponseType.SUCCESSFUL, data=request_params)
        elif request_type == ExchangeRequestType.BUY or request_type == ExchangeRequestType.SELL:
            # buy it
            self.__cash = self.__getCash()
            return ExchangeRequestResponse(status=ExchangeRequestResponseType.SUCCESSFUL, data=request_params)

    def add_asset(self, asset: Asset):
        """
        Add the asset to the exchange, then ensure the asset info is up-to-date. \n
        :param asset: the asset we are adding to the holdings.
        """
        if asset not in self.__holdings:
            self.__holdings.append(asset)
        else:
            request_type = ExchangeRequestType.UPDATE
            self.request(request_type=request_type, request_params=asset.toJSON(request_type=request_type))
