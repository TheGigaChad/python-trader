import enum
import json
from abc import ABC, abstractmethod
from typing import Optional, List

from yarl import URL

from pytrader import common


class ExchangeName(enum.Enum):
    """
     Enum used to identify the relevant exchange. \n
     """
    UNKNOWN = "UNKNOWN"
    ALPACA_PAPER = "ALPACA_PAPER"


class ExchangeType(enum.Enum):
    """
     Enum used to identify the relevant exchange type relating to what it can handle. \n
     """
    UNKNOWN = 0
    PAPER_STOCK = 1
    PAPER_CRYPTO = 2
    STOCK = 3
    CRYPTO = 4


class ExchangeRequestResponse:
    """
    Response from the exchange relating to the request.  This contains a status and optional data
    """

    def __init__(self, response_type: common.ResponseStatus, request_params=None, listen_required=False):
        self.__type: common.ResponseStatus = response_type
        self.__listen_required: bool = listen_required
        self.__data = request_params

    @property
    def type(self):
        return self.__type

    @property
    def data(self):
        return self.__data

    @property
    def listen_required(self):
        return self.__listen_required


class Exchange(ABC):
    """
    Class that holds the exchange type and name in order to classify what it can trade.
    """

    def __init__(self, name: ExchangeName, exchange_type: ExchangeType):
        self.__name: ExchangeName = name
        self.__type: ExchangeType = exchange_type
        self.__url: URL = self.get_url()
        self.__key: str = self.get_key()
        self.__secret: str = self.get_secret()
        self.__websocket: str = self.get_websocket()
        self.__cash: float = self.get_cash()
        self.__holdings: List[common.Asset] = self.get_holdings()
        self.__status: common.State = common.State.RUNNING

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def cash(self):
        return self.__cash

    @property
    def holdings(self) -> List[common.Asset]:
        return self.__holdings

    @property
    def key(self) -> str:
        return self.__key

    @property
    def secret(self) -> str:
        return self.__secret

    @property
    def websocket(self) -> str:
        return self.__websocket

    @abstractmethod
    def get_url(self) -> URL:
        """
        Returns the URL connection URL of the exchange. \n
        :return: URL.
        """

    @abstractmethod
    def get_key(self) -> str:
        """
        Returns the connection key of the exchange. \n
        :return: key.
        """

    @abstractmethod
    def get_secret(self) -> str:
        """
        Returns the connection secret of the exchange. \n
        :return: secret.
        """

    @abstractmethod
    def get_cash(self) -> float:
        """
        Returns the amount of cash held within the exchange. \n
        :return: cash value.
        """

    @abstractmethod
    def get_holdings(self) -> List[common.Asset]:
        """
        Returns the holdings within the exchange. \n
        :return: list of owned assets.
        """

    @abstractmethod
    def get_websocket(self) -> str:
        """
        Returns the websocket for the exchange. \n
        :return: websocket.
        """

    @abstractmethod
    def determine_allowance(self) -> float:
        """
        Returns an allowance for stock purchase
        """

    @abstractmethod
    def fulfill(self, order: common.Order) -> common.ResponseStatus:
        """
        Determines whether to buy or sell the stock.
        @param order: The order for the asset.
        @return: Status of the request.
        """

    @abstractmethod
    def buy(self, order: common.Order) -> bool:
        """
        the buy method for the exchange. \n
        :param order: the order that we are making a transaction on.
        :return: whether the buy was successful
        """

    @abstractmethod
    def buy_type(self):
        """
        determines the buy-type of the asset.  For now only supports market.
        :return: buy type
        """

    @abstractmethod
    def sell(self, order: common.Order) -> bool:
        """
        the sell method for the exchange. \n
        :param order: the order that we are making a transaction on.
        :return: whether the buy was successful
        """

    @abstractmethod
    def sell_type(self):
        """
        determines the sell-type of the asset.  For now only supports market.
        :return: sell type
        """

    @abstractmethod
    def request_allowance(self) -> float:
        """
        determines how much we alot the trade in terms of available funds.
        :return: the allotted allowance
        """
        # TODO - we need to consider how to assess this.

    @abstractmethod
    def request_quantity(self, asset: common.Asset) -> float:
        """
        determines the quantity of the asset.
        :param asset: the asset we are assessing.
        :return: the quantity.
        """

    @abstractmethod
    def get_trade_intent(self, asset: common.Asset) -> common.TradeIntent:
        """
        Determines the trade intent based on sql data.
        @param asset:
        @return:
        """

    @abstractmethod
    def update_order_status(self, order: common.Order) -> common.OrderStatus:
        """
        determines the order status based on the order id and the status within the exchange.
        @param order: the order being inspected
        @return: order status
        """

    @abstractmethod
    def determine_value(self, asset: common.Asset) -> float:
        """
        returns the current value of the asset.
        :param asset: asset being evaluated.
        :return: value in relative currency.
        """

    def get_stale_requests(self):
        """
        Finds any stale requests that may be lingering and re-adds them to the list.
        """
        pass

    def asset_to_json(self, request_type: Optional[common.RequestType] = common.RequestType.UNDEFINED) -> json:
        # TODO - this needs a lot of work
        """
        returns the asset information as a JSON item to be easily readable
        """
        if request_type == common.RequestType.UNDEFINED:
            return json.dumps(self)
        return json.dumps(self.__name)

    def add_asset(self, asset: common.Asset):
        """
        Add the asset to the exchange, then ensure the asset info is up-to-date. \n
        :param asset: the asset we are adding to the holdings.
        """
        if asset not in self.__holdings:
            self.__holdings.append(asset)
        else:
            request_type = common.RequestType.UPDATE
            self.request(request_type=request_type, request_params=self.asset_to_json(request_type=request_type))
