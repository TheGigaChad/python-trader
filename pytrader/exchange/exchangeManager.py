import time
from typing import Optional

from pydispatch import dispatcher

from pytrader.common.asset import Asset, AssetType
from pytrader.common.dispatch import Sender, Signal
from pytrader.common.order import Order, OrderStatus
from pytrader.common.status import Status
from pytrader.exchange.exchange import Exchange, ExchangeName, ExchangeType, RequestType, \
    ResponseType
from pytrader.exchange.exchange import ExchangeRequestResponse
from pytrader.exchange.exchangeListener import ExchangeListener


class ExchangeManager:
    # TODO - we might need a thread-lock here
    """
    Handles the exchanges and different types of requests etc.  This should be interacted with by the different managers.
    """

    def __init__(self, isTesting: Optional[bool] = False):
        self.__status = Status.UNKNOWN
        self.__sender: Sender = Sender.EXCHANGE_MANAGER
        self.__signal: Signal = Signal.EXCHANGE_MANAGER
        self.__order_queue: list[Order] = []
        self.__paper_stock_exchange = Exchange(exchange_type=ExchangeType.PAPER_STOCK, name=ExchangeName.ALPACA_PAPER)
        self.__paper_crypto_exchange = Exchange(exchange_type=ExchangeType.PAPER_CRYPTO, name=ExchangeName.ALPACA_PAPER)
        self.__stock_exchange = Exchange(exchange_type=ExchangeType.STOCK, name=ExchangeName.ALPACA_PAPER)
        self.__crypto_exchange = Exchange(exchange_type=ExchangeType.CRYPTO, name=ExchangeName.ALPACA_PAPER)
        self.__listener: ExchangeListener = ExchangeListener()
        self.__testing: bool = isTesting
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

    def __add_request_to_queue(self, order: Order):
        self.__order_queue.append(order)

    def __init(self):
        self.__status = Status.INIT
        dispatcher.connect(self.__dispatcher_receive, signal=Signal.TRADE_MANAGER.value,
                           sender=Signal.TRADE_MANAGER.value)

    def initialise(self):
        self.__init()
        self.__paper_stock_exchange.start()
        self.__paper_crypto_exchange.start()
        self.__stock_exchange.start()
        self.__crypto_exchange.start()
        self.__getStaleRequests()
        self.__status = Status.RUNNING
        print("EM STARTING")
        if not self.__testing:
            while 1:
                time.sleep(1)
                # check the queue status
                for order in self.__order_queue:
                    if order.status == OrderStatus.QUEUED or order.status == OrderStatus.INIT:
                        pass
                # save queue state to db(?)

                # commit trade

                # respond to trade manager on what we did

    def isRunning(self):
        return self.__status == Status.RUNNING

    def isIdle(self):
        return self.__status == Status.IDLE

    def isError(self):
        return self.__status == Status.ERROR

    def isStopped(self):
        return self.__status == Status.STOPPED

    def __is_new_order_unique(self, new_order: Order) -> bool:
        """
        determines whether new order should be added or not based on whether it exists in the queue already.
        @param new_order: the order we are checking already exists.
        @return: whether the order is unique and should be added.
        """
        for order in self.__order_queue:
            if order.asset.name == new_order.asset.name:
                if order.status == OrderStatus.PROCESSING or order.status == OrderStatus.FILLED or \
                        order.status == OrderStatus.QUEUED:
                    return False
        return True

    def __getStaleRequests(self):
        """
        returns all stale requests still sitting in exchanges.  This should be run on startup.
        """
        # TODO - search exchange requests for unfulfilled requests and return as a list of Requests
        self.__order_queue = []

    def __dispatcher_receive(self, message):
        """
        handle dispatcher response.  This is used to communicate with the other Managers.
        """
        if isinstance(message, Order):
            # If we get an order, add it to the queue if it is unique.
            if self.__is_new_order_unique(message):
                print(f"EM received order for {message.asset.name}, adding to queue.")
                message.status = OrderStatus.QUEUED
                response = ResponseType.SUCCESSFUL
                self.__add_request_to_queue(message)
            else:
                print(f"EM received a non-unique order for {message.asset.name}, cancelling the order.")
                message.status = OrderStatus.CANCELLED
                response = ResponseType.EXISTS
            # response = self.request(asset=message.asset, request_type=message.type)
            dispatcher.send(message=response, signal=self.__signal.value, sender=self.__sender.value)

    def request(self, asset: Asset, request_type: RequestType, request_params=None) -> ResponseType:
        """
        exchange request
        """

        #
        print(f"Request for {request_type.value} made for {asset.name}.")
        if asset.type == AssetType.PAPER_STOCK:
            response: ExchangeRequestResponse = self.__paper_stock_exchange.request(asset, request_type, request_params)
            print(f"Request for {request_type.value} made for {asset.name} is {response.type.value}.")
            if response.listen_required:
                # validation required that exchange received request (needed for buys/sells).
                # TODO - Add listener for trade confirmations
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
