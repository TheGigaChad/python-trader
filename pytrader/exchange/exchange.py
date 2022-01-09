import enum
import json
import random
from typing import Optional

from pytrader.common.asset import Asset
from pytrader.common.status import Status
from pytrader.common.requests import RequestType, ResponseType
from pytrader.config import ALPACA_PAPER_ADDRESS, ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, ALPACA_PAPER_WEBSOCKET
import alpaca_trade_api


class ExchangeName(enum.Enum):
    """
     Enum used to identify the relevant exchange. \n
     """
    UNKNOWN = "UNKNOWN"
    ALPACA_PAPER = "ALPACA-PAPER"


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

    def __init__(self, response_type: ResponseType, request_params=None, listen_required=False):
        self.__type: ResponseType = response_type
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


class Exchange:
    """
    Class that holds the exchange type and name in order to classify what it can trade.
    """

    def __init__(self, name: ExchangeName, exchange_type: ExchangeType):
        self.__status: Status = Status.UNKNOWN
        self.__name: ExchangeName = name
        self.__type: ExchangeType = exchange_type
        self.__url: str = self.__getURL()
        self.__key: str = self.__getKey()
        self.__secret: str = self.__getSecret()
        self.__websocket: str = self.__getWebsocket()
        self.__cash: float = 0.0
        self.__holdings: list[Asset] = []

    def __getURL(self) -> str:
        if self.__name == ExchangeName.ALPACA_PAPER:
            return ALPACA_PAPER_ADDRESS

    def __getKey(self) -> str:
        if self.__name == ExchangeName.ALPACA_PAPER:
            return ALPACA_PAPER_KEY

    def __getSecret(self) -> str:
        if self.__name == ExchangeName.ALPACA_PAPER:
            return ALPACA_PAPER_SECRET

    def __getCash(self) -> float:
        if self.__name == ExchangeName.ALPACA_PAPER:
            api = alpaca_trade_api.REST(self.__key, self.__secret, self.__url)
            cash = float(api.get_account().cash)
            api.close()
            return cash

    def __getHoldings(self) -> list[Asset]:
        api = alpaca_trade_api.REST(self.__key, self.__secret, self.__url)
        # print(api.list_assets())
        api.close()
        return []

    def __getWebsocket(self) -> str:
        if self.__name == ExchangeName.ALPACA_PAPER:
            return ALPACA_PAPER_WEBSOCKET

    def __init(self):
        self.__status = Status.INIT
        self.__cash = self.__getCash()
        self.__holdings = self.__getHoldings()

    def start(self):
        self.__init()
        self.__status = Status.RUNNING

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
    def holdings(self) -> list[Asset]:
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

    def __determineAllowance(self) -> float:
        """
        returns an allowance for stock purchase
        """
        return 1

    def __buy(self, asset: Asset):
        if self.__type == ExchangeType.PAPER_STOCK:
            api = alpaca_trade_api.REST(self.__key, self.__secret, self.__url)
            qty = self.__determineAllowance()
            order_id = "1" + str(random.randrange(1, 10000000))
            api.submit_order(symbol=asset.name, qty=qty, side="buy", type="market", client_order_id=order_id)
            api.close()

            return ExchangeRequestResponse(ResponseType.SUCCESSFUL, request_params=None, listen_required=True)

    def request(self, asset: Asset, request_type: RequestType, request_params=None):
        if request_type == RequestType.INFO:
            print(f"info requested for {asset.name} from the exchange {self.__name.value}")
        elif request_type == RequestType.UPDATE:
            # TODO - exchange logic
            return ExchangeRequestResponse(status=ResponseType.SUCCESSFUL)
        elif request_type == RequestType.INFO:
            return ExchangeRequestResponse(status=ResponseType.SUCCESSFUL, request_params=request_params)
        elif request_type == RequestType.BUY:
            return self.__buy(asset)

    def assetToJSON(self, request_type: Optional[RequestType] = RequestType.UNDEFINED) -> json:
        # TODO - this needs a lot of work
        """
        returns the asset information as a JSON item to be easily readable
        """
        if request_type == RequestType.UNDEFINED:
            return json.dumps(self)
        return json.dumps(self.__name)

    def add_asset(self, asset: Asset):
        """
        Add the asset to the exchange, then ensure the asset info is up-to-date. \n
        :param asset: the asset we are adding to the holdings.
        """
        if asset not in self.__holdings:
            self.__holdings.append(asset)
        else:
            request_type = RequestType.UPDATE
            self.request(request_type=request_type, request_params=self.assetToJSON(request_type=request_type))
