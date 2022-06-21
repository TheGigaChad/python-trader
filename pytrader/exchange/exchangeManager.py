import datetime
import time
from typing import Optional, List

from pydispatch import dispatcher

from pytrader import common, exchange, sql, config
from pytrader.sql import sqlDb

Log = common.Log(__file__)


class ExchangeManager:
    """
    Handles the exchanges and different types of requests etc. This should be interacted with by the different managers.
    """

    def __init__(self, run_type: Optional[common.RunType] = common.RunType.PRODUCTION):
        self.__status = common.State.UNKNOWN
        self.__sender: common.Sender = common.Sender.EXCHANGE_MANAGER
        self.__signal: common.Signal = common.Signal.EXCHANGE_MANAGER
        self.__order_queue: List[common.Order] = []
        self.__sql_manager: sql.SQLManager = sql.SQLManager()
        self.__paper_stock_exchange = exchange.ExchangeStockPaper()
        self.__run_type: common.RunType = run_type
        self.__trading_manager_status: common.State = common.State.UNKNOWN
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

    def fulfill_order(self, order: common.Order) -> common.GenericStatus:
        return self.__fulfill_order(order)

    def __add_order_to_queue(self, order: common.Order):
        """
        Adds the order to the order queue.
        :param order: order to be added.
        """
        self.__order_queue.append(order)

    def __generate_new_trade_id(self, order: common.Order) -> common.Order:
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

    def __fulfill_order(self, order: common.Order) -> common.GenericStatus:
        """
        Fulfills the order to the correct exchange.
        :param order: Order being requested.
        """
        # ensures the asset id is valid.
        order = self.__generate_new_trade_id(order)
        # fulfill to correct exchange
        if order.asset.type == common.AssetType.PAPER_STOCK:
            self.__paper_stock_exchange.fulfill(order)
        # update the order
        order.status = common.OrderStatus.PROCESSING
        order.asset.last_updated = datetime.datetime.now()

        # update sql tables
        response: sqlDb.SQLQueryResponseType = self.__sql_manager.open_trades_db.commit_trade(order)
        Log.i(f'Order to {order.type.name} {order.asset.qty} {order.asset.name} was {response.name}.')

        return common.GenericStatus.SUCCESSFUL

    def __remove_order(self, order: common.Order):
        """
        removes the order from the order queue and the open trades db and then adds it to the trade db. \n
        :param order: order being removed/added to trade db
        """
        response: sqlDb.SQLQueryResponseType = self.__sql_manager.trades_db.commit_trade(order)
        if response == sqlDb.SQLQueryResponseType.SUCCESSFUL:
            response = self.__sql_manager.open_trades_db.delete_trade(order)
            if response == sqlDb.SQLQueryResponseType.SUCCESSFUL:
                self.__order_queue.remove(order)

    def __reorder(self, order: common.Order):
        """
        Updates the order within the pending trade db.
        :param order: the order to be updated.
        """
        Log.w(f"Order for {order.asset.name} has timed out while processing. Let's re-order it.")
        # TODO - we need to reorder to correct exchange
        if order.asset.type == common.AssetType.PAPER_STOCK:
            pass
        elif order.asset.type == common.AssetType.STOCK:
            pass
        elif order.asset.type == common.AssetType.PAPER_CRYPTO:
            pass
        elif order.asset.type == common.AssetType.CRYPTO:
            pass
        elif order.asset.type == common.AssetType.FUND:
            pass

        order.asset.last_updated = datetime.datetime.now()
        self.__sql_manager.open_trades_db.update_trade(order)

    @staticmethod
    def __order_failed_or_timed_out_check(order: common.Order) -> bool:
        """
        returns whether the order has been unsuccessful or has timed out. \n
        :param order: the order to be checked.
        :return: the success of the transaction on the exchange.
        """
        if (datetime.datetime.now() - order.asset.last_updated).seconds >= config.USER_OPEN_TRADE_TIME_DELTA \
                and order.status == common.OrderStatus.PROCESSING:
            return True
        elif order.status == common.OrderStatus.CANCELLED:
            return True
        elif order.status == common.OrderStatus.FAILED:
            return True
        elif order.status == common.OrderStatus.REJECTED:
            return True
        else:
            return False

    def __init(self):
        self.__status = common.State.INIT
        dispatcher.connect(self.__dispatcher_receive, signal=common.Signal.TRADE_MANAGER.value,
                           sender=common.Signal.TRADE_MANAGER.value)

    def initialise(self):
        self.__init()
        self.__get_existing_open_trades()
        self.request_trading_manager_status()
        self.__status = common.State.READY
        if self.__run_type == common.RunType.PRODUCTION:
            while self.__trading_manager_status != common.State.READY:
                time.sleep(2)
                Log.i(f"initialise : re-requesting TM status. status is {self.__trading_manager_status}")
                self.request_trading_manager_status()
            self.__status = common.State.RUNNING
            while self.is_running():
                time.sleep(1)
                # TODO - this should be reactive or something
                for order in self.__order_queue:
                    if order.status == common.OrderStatus.QUEUED:
                        self.__fulfill_order(order)
                    elif order.status == common.OrderStatus.FILLED:
                        self.__remove_order(order)
                    elif self.__order_failed_or_timed_out_check(order):
                        self.__reorder(order)

    def is_running(self) -> bool:
        """
        Determines whether the manager is running.
        :return: running status
        """
        return self.__status == common.State.RUNNING

    def is_idle(self) -> bool:
        """
        Determines whether the manager is idle.
        :return: idle status
        """
        return self.__status == common.State.IDLE

    def is_error(self) -> bool:
        """
        Determines whether the manager is in an error state.
        :return: error status
        """
        return self.__status == common.State.ERROR

    def is_stopped(self) -> bool:
        """
        Determines whether the manager is stopped.
        :return: stopped status
        """
        return self.__status == common.State.STOPPED

    def request_trading_manager_status(self):
        """
        Requests the status of the Trading Manager. \n
        :return: none
        """
        dispatcher.send(status=common.ResponseStatus.NONE, request_type=common.RequestType.STATUS,
                        signal=self.__signal.value, sender=self.__sender.value)

    def __is_new_order_unique(self, new_order: common.Order) -> bool:
        """
        determines whether new order should be added or not based on whether it exists in the queue already. \n
        :param new_order: the order we are checking already exists.
        :return: whether the order is unique and should be added.
        """
        for order in self.__order_queue:
            if order.asset.name == new_order.asset.name:
                if order.status == common.OrderStatus.PROCESSING or order.status == common.OrderStatus.QUEUED:
                    return False
        return True

    def __get_assets_from_exchanges(self, asset_type: Optional[common.AssetType] = None) -> List[common.Asset]:
        """
        determines the assets held based on the asset type.  This will return all assets if you don't specify.
        :param asset_type: type of asset you want specifically.
        :return: all assets owned.
        """
        assets = None
        if asset_type is None:
            paper_stock = self.__paper_stock_exchange.holdings
            assets = paper_stock
        elif asset_type == common.AssetType.PAPER_STOCK:
            paper_stock = self.__paper_stock_exchange.holdings
            assets = paper_stock
        elif asset_type == common.AssetType.PAPER_CRYPTO:
            pass
        elif asset_type == common.AssetType.STOCK:
            pass
        elif asset_type == common.AssetType.CRYPTO:
            pass
        return assets

    def __update_order_status_from_exchange(self, order: common.Order) -> common.Order:
        """
        updates the order status based on whether the exchange has filled the order, received it or not. \n
        :param order: the order being evaluated.
        :return: updated order.
        """
        if order.asset.type == common.AssetType.PAPER_STOCK:
            return self.__paper_stock_exchange.update_order_status(order)
        elif order.asset.type == common.AssetType.STOCK:
            pass
        elif order.asset.type == common.AssetType.PAPER_CRYPTO:
            pass
        elif order.asset.type == common.AssetType.CRYPTO:
            pass
        elif order.asset.type == common.AssetType.FUND:
            pass
        else:
            Log.w(f"Attempted to update the order status for {order} but cannot evaluate correct asset type.")
            return order

    def __evaluate_order_value(self, order: common.Order) -> float:
        """
        evaluates the current value of the asset.
        :param order: order being evaluated
        :return: value
        """
        value = 0.0
        if order.asset.type == common.AssetType.PAPER_STOCK:
            value = self.__paper_stock_exchange.determine_value(order.asset)
        else:
            pass
        return value

    def __open_trade_dao_to_order(self, open_trade: sqlDb.daos.SQLDbOpenTradesDao) -> common.Order:
        """
        creates an order from the dao object.
        :param open_trade: dao object
        :return: order.
        """
        order: common.Order = common.Order(common.OrderType(open_trade.order_type),
                                           common.Asset(name=open_trade.name,
                                                        asset_type=common.AssetType(open_trade.asset_type)))
        order.asset.id = open_trade.order_id
        order.asset.qty = open_trade.quantity
        order.asset.trade_intent = common.TradeIntent(open_trade.trade_intent)
        order.asset.last_updated = open_trade.timestamp
        order.asset.value = self.__evaluate_order_value(order)
        return order

    def __get_existing_open_trades(self):
        """
        Finds all open trades within the exchanges and appends them to the queue. \n
        :return: none
        """
        if self.__run_type == common.RunType.TEST:
            return
        open_trades: [sqlDb.daos.SQLDbOpenTradesDao] = self.__sql_manager.open_trades_db.get_all_trades()
        for open_trade in open_trades:
            new_order: common.Order = self.__open_trade_dao_to_order(open_trade)
            self.__update_order_status_from_exchange(new_order)
            if self.__is_new_order_unique(new_order):
                self.__order_queue.append(new_order)
            else:
                Log.w(f"__get_stale_requests has found order duplicate for order {new_order}")
        Log.i(f"found {len(self.__order_queue)} existing orders. They have been added to the order queue successfully.")

    def __dispatcher_receive_order_request(self, order: common.Order):
        """
        Handles the receiving of an order from the Trading Manager.
        :param order: the order request.
        """
        # add it to the queue if it is unique and send response back to Trading Manager.
        if self.__is_new_order_unique(order):
            Log.i(f"{order.asset.name} is unique, adding to queue.")
            order.status = common.OrderStatus.QUEUED
            status = common.ResponseStatus.SUCCESSFUL
            self.__add_order_to_queue(order)

        else:
            Log.w(f"EM received a non-unique order for {order.asset.name}, cancelling the order.")
            order.status = common.OrderStatus.CANCELLED
            status = common.ResponseStatus.EXISTS
        dispatcher.send(status=status, response_type=common.ResponseType.TRADE, order=order, signal=self.__signal.value,
                        sender=self.__sender.value)

    def __dispatcher_receive_holdings_request(self):
        """
        Handles the receiving of a request for holdings from the Trading Manager.
        :return: none
        """
        holdings = self.__get_assets_from_exchanges()
        status = common.ResponseStatus.SUCCESSFUL if holdings is not None else common.ResponseStatus.UNSUCCESSFUL
        dispatcher.send(status=status, response_type=common.ResponseType.HOLDINGS, holdings=holdings,
                        signal=self.__signal.value,
                        sender=self.__sender.value)

    def __dispatcher_receive_allowance_request(self, order: common.Order):
        """
        Handles the receiving of a request for an allowance from the Trading Manager.
        :param order: the order we are requesting an allowance for.
        """
        if order.asset.type == common.AssetType.PAPER_STOCK:
            order.asset.value = self.__paper_stock_exchange.request_allowance()
            if order.asset.value >= 0.0:
                order.asset.qty = self.__paper_stock_exchange.request_quantity(asset=order.asset)
                if order.asset.qty >= 0.0:
                    dispatcher.send(response_type=common.ResponseType.ALLOWANCE,
                                    status=common.ResponseStatus.SUCCESSFUL,
                                    order=order, signal=self.__signal.value, sender=self.__sender.value)
                    return
            Log.w(f"__dispatcher_receive_allowance_request : bad order value ({order.asset.value})"
                  f" or quantity ({order.asset.qty})")
            dispatcher.send(response_type=common.ResponseType.ALLOWANCE, status=common.ResponseStatus.UNSUCCESSFUL,
                            order=order, signal=self.__signal.value, sender=self.__sender.value)

    def __dispatcher_receive_status_request(self):
        """
        Handles the status request response from the Trading Manager.
        """
        dispatcher.send(status=common.ResponseStatus.SUCCESSFUL, response_type=common.ResponseType.STATUS,
                        manager_status=self.__status, signal=self.__signal.value, sender=self.__sender.value)

    def __dispatcher_receive_thresholds_request(self, asset: common.Asset):
        """
        Handles the buy and sell threshold requests from the Trading Manager.
        :return:
        """
        buy_threshold, sell_threshold = self.__sql_manager.buy_sell_threshold_db.get_threshold(asset)
        dispatcher.send(status=common.ResponseStatus.SUCCESSFUL, response_type=common.ResponseType.BUY_SELL_THRESHOLDS,
                        buy_threshold=buy_threshold, sell_threshold=sell_threshold, asset=asset,
                        signal=self.__signal.value, sender=self.__sender.value)

    def __dispatcher_receive_status_response(self, status: common.State):
        """
        Handles the status response from the Trading Manager.
        :param status: the status of the Trading Manager.
        """
        self.__trading_manager_status = status

    def __dispatcher_receive(self, **kwargs):
        """
        handle dispatcher response.  This is used to communicate with the other Managers.
        """
        request_type: Optional[common.RequestType] = kwargs.get("request_type")
        response_type: Optional[common.ResponseType] = kwargs.get("response_type")
        if request_type is not None:
            if request_type == common.RequestType.TRADE:
                self.__dispatcher_receive_order_request(kwargs.get("order"))
            elif request_type == common.RequestType.HOLDINGS:
                self.__dispatcher_receive_holdings_request()
            elif request_type == common.RequestType.ALLOWANCE:
                self.__dispatcher_receive_allowance_request(kwargs.get("order"))
            elif request_type == common.RequestType.STATUS:
                self.__dispatcher_receive_status_request()
            elif request_type == common.RequestType.BUY_SELL_THRESHOLDS:
                self.__dispatcher_receive_thresholds_request(kwargs.get("asset"))
        elif response_type is not None:
            if response_type == common.ResponseType.STATUS:
                self.__dispatcher_receive_status_response(kwargs.get("manager_status"))
        else:
            Log.w(f"__dispatcher_receive : received a bad request ({request_type}) and/or  response ({response_type}).")
