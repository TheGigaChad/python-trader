import json
from typing import Optional

from pytrader.exchange.exchange import Exchange, ExchangeName, ExchangeType, RequestType, \
    ResponseType
from pytrader.common.asset import Asset, AssetType
from pytrader.common.status import Status
from pytrader.common.requests import Request
from pytrader.exchange.exchangeListener import ExchangeListener
from pytrader.exchange.exchange import ExchangeRequestResponse


class ExchangeManager:
    # TODO - we might need a thread-lock here
    """
    Handles the exchanges and different types of requests etc.  This should be interacted with by the different managers.
    """
    def __init__(self):
        self.__status = Status.UNKNOWN
        self.__request_queue: list[Request] = []
        self.__paper_stock_exchange  = Exchange(exchange_type=ExchangeType.PAPER_STOCK, name=ExchangeName.ALPACA_PAPER)
        self.__paper_crypto_exchange = Exchange(exchange_type=ExchangeType.PAPER_CRYPTO, name=ExchangeName.ALPACA_PAPER)
        self.__stock_exchange = Exchange(exchange_type=ExchangeType.STOCK, name=ExchangeName.ALPACA_PAPER)
        self.__crypto_exchange = Exchange(exchange_type=ExchangeType.CRYPTO, name=ExchangeName.ALPACA_PAPER)
        self.__listener: ExchangeListener = ExchangeListener()
        self.initialise()

    @property
    def paper_stock_exchange(self):
        return self.__paper_stock_exchange

    @property
    def paper_crypto_exchange(self):
        return self.__paper_crypto_exchange

    @property
    def stock_exchange(self):
        return self.stock_exchange

    @property
    def crypto_exchange(self):
        return self.crypto_exchange

    def __init(self):
        self.__status = Status.INIT

    def initialise(self):
        self.__init()
        self.__paper_stock_exchange.start()
        self.__paper_crypto_exchange.start()
        self.__stock_exchange.start()
        self.__crypto_exchange.start()
        self.__getStaleRequests()
        self.__status = Status.RUNNING

    def isRunning(self):
        return self.__status == Status.RUNNING

    def isIdle(self):
        return self.__status == Status.IDLE

    def isError(self):
        return self.__status == Status.ERROR

    def isStopped(self):
        return self.__status == Status.STOPPED

    def __getStaleRequests(self):
        """
        returns all stale requests still sitting in exchanges.  This should be run on startup.
        """
        # TODO - search exchange requests for unfulfilled requests and return as a list of Requests
        self.__request_queue = []

    def request(self, asset: Asset, request_type: RequestType, request_params=None) \
            -> ResponseType:
        """
        exchange request
        """
        print(f"Request for {request_type.value} made for {asset.name}.")
        if asset.type == AssetType.PAPER_STOCK:
            response: ExchangeRequestResponse = self.__paper_stock_exchange.request(asset, request_type, request_params)
            print(f"Request for {request_type.value} made for {asset.name} is {response.type.value}.")
            if response.listen_required:
                # validation required that exchange received request (needed for buys/sells).
                return self.__listener.listen_for(response.data, self.__paper_stock_exchange)
            else:
                return response.type

    def update(self):
        """
        Call to update data on all exchanges.
        """
        self.__paper_stock_exchange.request(RequestType.UPDATE)
        self.__paper_crypto_exchange.request(RequestType.UPDATE)

    def getAssets(self, asset_type: Optional[AssetType] = AssetType.UNKNOWN) -> list[Asset]:
        """
        determines the assets held based on the asset type.  This will return all assets if you don't specify.
        :param asset_type: type of asset you want specifically.
        :return: all assets owned.
        """
        assets = None
        if asset_type == AssetType.UNKNOWN:
            paper_stock = self.__paper_stock_exchange.holdings
            paper_crypto = self.__paper_crypto_exchange.holdings
            stock = self.__stock_exchange.holdings
            crypto = self.__crypto_exchange.holdings
            assets = paper_stock
            assets.extend(paper_crypto)
            assets.extend(stock)
            assets.extend(crypto)
        elif asset_type == AssetType.PAPER_STOCK:
            assets = self.__paper_stock_exchange.holdings
        elif asset_type == AssetType.PAPER_CRYPTO:
            assets = self.__paper_crypto_exchange.holdings
        elif asset_type == AssetType.STOCK:
            assets = self.__stock_exchange.holdings
        elif asset_type == AssetType.CRYPTO:
            assets = self.__crypto_exchange.holdings
        return assets


