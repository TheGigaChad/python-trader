import datetime
import time
from typing import Optional, List

from pydispatch import dispatcher

from pytrader.SQL.sqlDb.Daos.sqlDbOpenTradesDao import SQLDbOpenTradesDao
from pytrader.SQL.sqlDb.sqlDb import SQLQueryResponseType
from pytrader.SQL.sqlDbManager import SQLDbManager
from pytrader.algo.algo_tradeIntent import TradeIntent
from pytrader.common.asset import Asset, AssetType
from pytrader.common.dispatch import Sender, Signal
from pytrader.common.log import Log
from pytrader.common.order import Order, OrderStatus, OrderType
from pytrader.common.requests import ResponseType
from pytrader.common.status import Status
from pytrader.config import USER_OPEN_TRADE_TIME_DELTA
from pytrader.exchange.exchange import RequestType, \
    ResponseStatus
from pytrader.exchange.exchangeStockPaper import ExchangeStockPaper

Log = Log(__file__)


class ExchangeManager:
    """
    Handles the exchanges and different types of requests etc.  This should be interacted with by the different managers.
    """

    def __init__(self, is_testing: Optional[bool] = False):
        self.__status = Status.UNKNOWN
        self.__sender: Sender = Sender.EXCHANGE_MANAGER
        self.__signal: Signal = Signal.EXCHANGE_MANAGER
        self.__order_queue: List[Order] = []
        self.__sql_manager: SQLDbManager = SQLDbManager()
        self.__paper_stock_exchange = ExchangeStockPaper()
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
        """
        Adds the order to the order queue.
        :param order: order to be added.
        """
        self.__order_queue.append(order)

    def __generate_new_trade_id(self, order: Order) -> Order:
        """
        Generates a unique id based on existing ids within the open and trades dbs. \n
        :param order: the order we are generating an ID for.
        :return: order with updated ID.
        """
        if order.asset.id == 0:
            order.asset.id = self.__sql_manager.open_trades_db.generate_new_asset_id(order)
            while not self.__sql_manager.trades_db.is_order_id_unique(order.asset.id):
                order.asset.id = self.__sql_manager.open_trades_db.generate_new_asset_id(order)
        return order

    def __fulfill_order(self, order: Order):
        """
        Fulfills the order to the correct exchange.
        :param order: Order being requested.
        """
        # ensures the asset id is valid.
        order = self.__generate_new_trade_id(order)
        # fulfill to correct exchange
        if order.asset.type == AssetType.PAPER_STOCK:
            self.__paper_stock_exchange.fulfill(order)
        # update the order
        order.status = OrderStatus.PROCESSING
        order.asset.last_updated = datetime.datetime.now()

        # update SQL tables
        response: SQLQueryResponseType = self.__sql_manager.open_trades_db.commit_trade(order)
        Log.i(f'Order to {order.type.name} {order.asset.qty} {order.asset.name} was {response.name}.')

    def __remove_order(self, order: Order):
        """
        removes the order from the order queue and the open trades db and then adds it to the trade db. \n
        :param order: order being removed/added to trade db
        """
        response: SQLQueryResponseType = self.__sql_manager.trades_db.commit_trade(order)
        if response == SQLQueryResponseType.SUCCESSFUL:
            response = self.__sql_manager.open_trades_db.delete_trade(order)
            if response == SQLQueryResponseType.SUCCESSFUL:
                self.__order_queue.remove(order)

    def __reorder(self, order: Order):
        """
        Updates the order within the pending trade db.
        :param order: the order to be updated.
        """
        Log.w(f"Order for {order.asset.name} has timed out while processing. Let's re-order it.")
        # TODO - we need to reorder to correct exchange
        if order.asset.type == AssetType.PAPER_STOCK:
            pass
        elif order.asset.type == AssetType.STOCK:
            pass
        elif order.asset.type == AssetType.PAPER_CRYPTO:
            pass
        elif order.asset.type == AssetType.CRYPTO:
            pass
        elif order.asset.type == AssetType.FUND:
            pass

        order.asset.last_updated = datetime.datetime.now()
        self.__sql_manager.open_trades_db.update_trade(order)

    @staticmethod
    def __order_failed_or_timed_out(order: Order) -> bool:
        """
        returns whether the order has been unsuccessful or has timed out. \n
        :param order: the order to be checked.
        :return: the success of the transaction on the exchange.
        """
        if (datetime.datetime.now() - order.asset.last_updated).seconds >= USER_OPEN_TRADE_TIME_DELTA \
                and order.status == OrderStatus.PROCESSING:
            return True
        elif order.status == OrderStatus.CANCELLED:
            return True
        elif order.status == OrderStatus.FAILED:
            return True
        elif order.status == OrderStatus.REJECTED:
            return True
        else:
            return False

    def __init(self):
        self.__status = Status.INIT
        dispatcher.connect(self.__dispatcher_receive, signal=Signal.TRADE_MANAGER.value,
                           sender=Signal.TRADE_MANAGER.value)

    def initialise(self):
        self.__init()
        self.__get_existing_open_trades()
        self.request_trading_manager_status()
        self.__status = Status.READY
        if not self.__testing:
            while self.__trading_manager_status != Status.READY:
                time.sleep(2)
                Log.i(f"initialise : re-requesting TM status. status is {self.__trading_manager_status}")
                self.request_trading_manager_status()
            self.__status = Status.RUNNING
            while self.is_running():
                time.sleep(1)
                # TODO - this should be reactive or something
                for order in self.__order_queue:
                    print(order)
                    if order.status == OrderStatus.QUEUED:
                        self.__fulfill_order(order)
                    elif order.status == OrderStatus.FILLED:
                        self.__remove_order(order)
                    elif self.__order_failed_or_timed_out(order):
                        self.__reorder(order)

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
                if order.status == OrderStatus.PROCESSING or order.status == OrderStatus.QUEUED:
                    return False
        return True

    def __update_order_status_from_exchange(self, order) -> Order:
        """
        updates the order status based on whether the exchange has filled the order, received it or not.
        :param order: the order being evaluated.
        :return: updated order.
        """
        if order.asset.type == AssetType.PAPER_STOCK:
            return self.__paper_stock_exchange.update_order_status(order)
        elif order.asset.type == AssetType.STOCK:
            pass
        elif order.asset.type == AssetType.PAPER_CRYPTO:
            pass
        elif order.asset.type == AssetType.CRYPTO:
            pass
        elif order.asset.type == AssetType.FUND:
            pass
        else:
            Log.w(f"Attempted to update the order status for {order} but cannot evaluate correct asset type.")
            return order

    def __evaluate_order_value(self, order) -> float:
        """
        evaluates the current value of the asset.
        :param order: order being evaluated
        :return: value
        """
        value = 0.0
        if order.asset.type == AssetType.PAPER_STOCK:
            value = self.__paper_stock_exchange.determine_value(order.asset)
        else:
            pass
        return value

    def __open_trade_dao_to_order(self, open_trade: SQLDbOpenTradesDao) -> Order:
        """
        creates an order from the dao object.
        :param open_trade: dao object
        :return: order.
        """
        order: Order = Order(OrderType(open_trade.order_type),
                             Asset(name=open_trade.name, asset_type=AssetType(open_trade.asset_type)))
        order.asset.id = open_trade.order_id
        order.asset.qty = open_trade.quantity
        order.asset.trade_intent = TradeIntent(open_trade.trade_intent)
        order.asset.last_updated = open_trade.timestamp
        order.asset.value = self.__evaluate_order_value(order)
        return order

    def __get_existing_open_trades(self):
        """
        Finds all open trades within the exchanges and appends them to the queue if they are not filled yet. \n
        """
        if self.__testing:
            return
        open_trades: [SQLDbOpenTradesDao] = self.__sql_manager.open_trades_db.get_all_trades()
        for open_trade in open_trades:
            new_order: Order = self.__open_trade_dao_to_order(open_trade)
            self.__update_order_status_from_exchange(new_order)
            if self.__is_new_order_unique(new_order):
                self.__order_queue.append(new_order)
            else:
                Log.w(f"__get_stale_requests has found order duplicate for order {new_order}")
        Log.i(f"found {len(self.__order_queue)} existing orders. They have been added to the order queue successfully.")

    def __dispatcher_receive_order_request(self, order: Order):
        """
        Handles the receiving of an order from the Trading Manager.
        :param order: the order request.
        """
        # add it to the queue if it is unique and send response back to Trading Manager.
        if self.__is_new_order_unique(order):
            Log.i(f"{order.asset.name} is unique, adding to queue.")
            order.status = OrderStatus.QUEUED
            status = ResponseStatus.SUCCESSFUL
            self.__add_order_to_queue(order)

        else:
            Log.w(f"EM received a non-unique order for {order.asset.name}, cancelling the order.")
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
            Log.w(f"__dispatcher_receive_allowance_request : bad order value ({order.asset.value})"
                  f" or quantity ({order.asset.qty})")
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
            Log.w(f"__dispatcher_receive : received a bad request ({request_type}) and/or  response ({response_type}).")

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
