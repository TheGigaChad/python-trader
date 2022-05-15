import time
from typing import Optional, List

from pydispatch import dispatcher

from pytrader.common.asset import Asset, AssetType
from pytrader.common.dispatch import Sender, Signal
from pytrader.common.order import Order, OrderStatus
from pytrader.common.requests import ResponseType
from pytrader.common.status import Status
from pytrader.exchange.exchange import ExchangeRequestResponse
from pytrader.exchange.exchange import RequestType, \
    ResponseStatus
from pytrader.exchange.exchangeListener import ExchangeListener
from pytrader.exchange.exchangeStockPaper import ExchangeStockPaper


class ExchangeManager:
    """
    Handles the exchanges and different types of requests etc.  This should be interacted with by the different managers.
    """

    def __init__(self, is_testing: Optional[bool] = False):
        self.__status = Status.UNKNOWN
        self.__sender: Sender = Sender.EXCHANGE_MANAGER
        self.__signal: Signal = Signal.EXCHANGE_MANAGER
        self.__order_queue: List[Order] = []
        self.__paper_stock_exchange = ExchangeStockPaper()
        self.__listener: ExchangeListener = ExchangeListener()
        self.__testing: bool = is_testing
        self.__trading_manager_status: Status = Status.UNKNOWN
        self.initialise()

    @property
    def paper_stock_exchange(self):
        return self.__paper_stock_exchange

    @property
    def stock_exchange(self):
        return self.stock_exchange

    @property
    def crypto_exchange(self):
        return self.crypto_exchange

    def __add_order_to_queue(self, order: Order):
        self.__order_queue.append(order)

    def __init(self):
        self.__status = Status.INIT
        dispatcher.connect(self.__dispatcher_receive, signal=Signal.TRADE_MANAGER.value,
                           sender=Signal.TRADE_MANAGER.value)

    def initialise(self):
        self.__init()
        self.__get_stale_requests()
        self.request_trading_manager_status()
        self.__status = Status.READY
        if not self.__testing:
            while self.__trading_manager_status != Status.READY:
                time.sleep(2)
                print(f"EM re-requesting TM status. status is {self.__trading_manager_status}")
                self.request_trading_manager_status()
            self.__status = Status.RUNNING
            print(f"ExchangeManager is {self.__status.name}.")
            while 1:
                time.sleep(1)
                # check the queue status
                for order in self.__order_queue:
                    if order.status == OrderStatus.QUEUED:
                        print(order)
                print("-------------")

                # save queue state to db(?)

                # commit trade

                # respond to trade manager on what we did

    def is_running(self) -> bool:
        """
        Determines whether the manager is running.
        :return: running status
        """
        return self.__status == Status.RUNNING

    def is_idle(self) -> bool:
        """
        Determines whether the manager is idle.
        :return: idle status
        """
        return self.__status == Status.IDLE

    def is_error(self) -> bool:
        """
        Determines whether the manager is in an error state.
        :return: error status
        """
        return self.__status == Status.ERROR

    def is_stopped(self) -> bool:
        """
        Determines whether the manager is stopped.
        :return: stopped status
        """
        return self.__status == Status.STOPPED

    def request_trading_manager_status(self):
        """
        Requests the status of the Trading Manager.
        """
        dispatcher.send(status=ResponseStatus.NONE, request_type=RequestType.STATUS, signal=self.__signal.value,
                        sender=self.__sender.value)

    def __is_new_order_unique(self, new_order: Order) -> bool:
        """
        determines whether new order should be added or not based on whether it exists in the queue already. \n
        :param new_order: the order we are checking already exists.
        :return: whether the order is unique and should be added.
        """
        for order in self.__order_queue:
            if order.asset.name == new_order.asset.name:
                if order.status == OrderStatus.PROCESSING or order.status == OrderStatus.FILLED or \
                        order.status == OrderStatus.QUEUED:
                    return False
        return True

    def __get_stale_requests(self):
        """
        returns all stale requests still sitting in exchanges.  This should be run on startup.
        """
        # TODO - search exchange requests for unfulfilled requests and return as a list of Requests
        # self.__order_queue = []
        pass

    def __dispatcher_receive_order_request(self, order: Order):
        """
        Handles the receiving of an order from the Trading Manager.
        :param order: the order request.
        """
        # add it to the queue if it is unique and send response back to Trading Manager.
        print(f"EM received order for {order.asset.name}, adding to queue.")
        if self.__is_new_order_unique(order):
            print(f"{order.asset.name} is unique, adding to queue.")
            order.status = OrderStatus.QUEUED
            status = ResponseStatus.SUCCESSFUL
            self.__add_order_to_queue(order)

        else:
            print(f"EM received a non-unique order for {order.asset.name}, cancelling the order.")
            order.status = OrderStatus.CANCELLED
            status = ResponseStatus.EXISTS
        dispatcher.send(status=status, response_type=ResponseType.TRADE, order=order, signal=self.__signal.value,
                        sender=self.__sender.value)

    def __dispatcher_receive_holdings_request(self):
        """
        Handles the receiving of a request for holdings from the Trading Manager.
        """
        holdings = self.get_assets()
        status = ResponseStatus.SUCCESSFUL if holdings is not None else ResponseStatus.UNSUCCESSFUL
        dispatcher.send(status=status, response_type=ResponseType.HOLDINGS, holdings=holdings,
                        signal=self.__signal.value,
                        sender=self.__sender.value)

    def __dispatcher_receive_allowance_request(self, order: Order):
        """
        Handles the receiving of a request for an allowance from the Trading Manager.
        :param order: the order we are requesting an allowance for.
        """
        if order.asset.type == AssetType.PAPER_STOCK:
            order.asset.value = self.__paper_stock_exchange.request_allowance()
            if order.asset.value >= 0.0:
                order.asset.qty = self.__paper_stock_exchange.request_quantity(asset=order.asset)
                if order.asset.qty >= 0.0:
                    dispatcher.send(response_type=ResponseType.ALLOWANCE, status=ResponseStatus.SUCCESSFUL,
                                    order=order, signal=self.__signal.value, sender=self.__sender.value)
                    return
            print(f"qty, value no good")
            dispatcher.send(response_type=ResponseType.ALLOWANCE, status=ResponseStatus.UNSUCCESSFUL,
                            order=order, signal=self.__signal.value, sender=self.__sender.value)

    def __dispatcher_receive_status_request(self):
        """
        Handles the status request response from the Trading Manager.
        """
        dispatcher.send(status=ResponseStatus.SUCCESSFUL, response_type=ResponseType.STATUS,
                        manager_status=self.__status, signal=self.__signal.value, sender=self.__sender.value)

    def __dispatcher_receive_status_response(self, status: Status):
        """
        Handles the status response from the Trading Manager.
        :param status: the status of the Trading Manager.
        """
        self.__trading_manager_status = status

    def __dispatcher_receive(self, **kwargs):
        """
        handle dispatcher response.  This is used to communicate with the other Managers.
        """
        request_type: Optional[RequestType] = kwargs.get("request_type")
        response_type: Optional[ResponseType] = kwargs.get("response_type")
        if request_type is not None:
            if request_type == RequestType.TRADE:
                self.__dispatcher_receive_order_request(kwargs.get("order"))
            elif request_type == RequestType.HOLDINGS:
                self.__dispatcher_receive_holdings_request()
            elif request_type == RequestType.ALLOWANCE:
                self.__dispatcher_receive_allowance_request(kwargs.get("order"))
            elif request_type == RequestType.STATUS:
                self.__dispatcher_receive_status_request()
        elif response_type is not None:
            if response_type == ResponseType.STATUS:
                self.__dispatcher_receive_status_response(kwargs.get("manager_status"))
        else:
            print(f"TM.__dispatcher_receive received a bad request/response. both None.")

    def request(self, asset: Asset, request_type: RequestType, request_params=None) -> ResponseStatus:
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

    def get_assets(self, asset_type: Optional[AssetType] = None) -> List[Asset]:
        """
        determines the assets held based on the asset type.  This will return all assets if you don't specify.
        :param asset_type: type of asset you want specifically.
        :return: all assets owned.
        """
        assets = None
        if asset_type is None:
            paper_stock = self.__paper_stock_exchange.holdings
            assets = paper_stock
        elif asset_type == AssetType.PAPER_STOCK:
            paper_stock = self.__paper_stock_exchange.holdings
            assets = paper_stock
        elif asset_type == AssetType.PAPER_CRYPTO:
            pass
        elif asset_type == AssetType.STOCK:
            pass
        elif asset_type == AssetType.CRYPTO:
            pass
        return assets
