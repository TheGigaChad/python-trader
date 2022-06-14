import datetime
import random
import time
from typing import Optional, List, Tuple

from pydispatch import dispatcher

from pytrader.common.asset import Asset, AssetType
from pytrader.common.dispatch import Sender, Signal
from pytrader.common.log import Log
from pytrader.common.order import Order, OrderType, OrderStatus
from pytrader.common.requests import ResponseStatus, RequestType, ResponseType
from pytrader.common.status import Status
from pytrader.common.tradeIntent import TradeIntent
from pytrader.config import DEV_TEST_MODE
from pytrader.sql.sqlDb.sqlDb import SQLDb, SQLDbType, SQLQueryResponseType

Log = Log(__file__)


def determine_buy_or_sell(confidence: float, asset: Asset) -> Optional[OrderType]:
    """
    determines whether we should buy, sell or ignore the asset based on the confidence value.
    :param confidence: float value relating to how good of a trade is available.
    :param asset: the asset we are inspecting.
    :return: boolean for whether we should buy/sell or ignore
    """
    buy_threshold, sell_threshold = determine_buy_sell_threshold_values(asset.name)
    if confidence >= buy_threshold:
        return OrderType.BUY
    elif confidence <= sell_threshold:
        return OrderType.SELL
    else:
        return None


def determine_buy_sell_threshold_values(asset_name: Asset.name) -> Optional[Tuple[float, float]]:
    """
    return the buy and sell threshold values for the relevant asset.
    :param asset_name: the asset name we are inspecting.
    :return: buy/sell threshold values as tuple.  Buy is first, second is sell.
    """
    # TODO - TIDY.....
    db: SQLDb = SQLDb(SQLDbType.BUY_SELL_THRESHOLDS)
    rows, headers = db.run_sql_query(f"SELECT buy, sell FROM {db.table_name} WHERE name = '{asset_name}';")
    if len(rows) == 1:
        return rows[0][0], rows[0][1]
    else:
        Log.d(f"tradingManager.determineBuySellThresholdValues - no db entry for {asset_name}. creating now...")
        query = f"INSERT INTO {db.table_name} (`name`, `buy`, `sell`, `last_updated`) VALUES (%s, '1.0','-1.0',%s);"
        params = [asset_name, datetime.datetime.now().__str__()]
        success: SQLQueryResponseType = db.run_sql_query_no_response(query, params)
        if success:
            rows, headers = db.run_sql_query(f"SELECT buy, sell FROM {db.table_name} WHERE name = '{asset_name}';")
            return rows[0][0], rows[0][1]
        Log.w(f"determineBuySellThresholdValues - couldn't create new entry for {asset_name}.")

    return None


def analyse_asset(asset: Asset) -> float:
    """
    Processes the asset based on in-built methodologies in order to determine the confidence value of the stock.
    A high value will constitute a purchase opportunity, a low value will mean a sell opportunity.
    :param asset: asset to be analysed.
    :return: confidence value.
    """
    # TODO - analyseAsset() logic
    return random.randrange(-10, 10, 1) + random.random()


def find_new_asset() -> Asset:
    """
    returns a new asset that will be used for inspection for buy/sell opportunities.
    """
    # TODO - create findNewAsset() logic
    return Asset("TSLA", AssetType.PAPER_STOCK)


def calculate_quantity(asset: Asset, confidence: float) -> float:
    """
    returns the quantity of stocks for the order. \n
    :param confidence: float value relating to how good of a trade is available. (low = sell, buy = high)
    :param asset: the asset we are inspecting.
    :return: how many stocks
    """
    # TODO - calculateQuantity() logic
    return 1.0


def calculate_value(asset: Asset, qty: float) -> float:
    """
    calculates the value of the asset based on how much is owned.
    @param asset:
    @param qty:
    @return:
    """
    return 1.0


def create_order(asset: Asset, order_type: OrderType) -> Order:
    """
    create an order for the asset based on the confidence value. \n
    :param asset: the asset we are inspecting.
    :param order_type: the order type we are receiving.
    :return: boolean for whether we should buy/sell or ignore
    """
    return Order(order_type, asset)


class TradingManager:
    """
    The manager that will handle all the trading based on predetermined models.  It will also look for new potential
    trades.
    """

    def __init__(self):
        self.__threads = None
        self.__status = Status.STARTING
        self.__assets: Optional[List[Asset]] = None
        self.__sender: Sender = Sender.TRADE_MANAGER
        self.__signal: Signal = Signal.TRADE_MANAGER
        self.__exchange_manager_status: Status = Status.UNKNOWN
        self.start()

    @property
    def status(self):
        return self.__status

    def start(self):
        """
        Starts the dispatcher to the exchange manager.
        """
        Log.d("TradingManager is starting.")
        dispatcher.connect(self.__dispatcher_receive, signal=Signal.EXCHANGE_MANAGER.value,
                           sender=Signal.EXCHANGE_MANAGER.value)

        # TODO - probe ALL exchanges for asset list
        self.__status = Status.STARTING
        Log.d("TradingManager is waiting on Exchange Manager for the list of owned assets.")
        while self.__assets is None:
            # wait for the list of owned assets.
            time.sleep(3)
            self.__get_owned_assets()
        self.__status = Status.READY
        while self.__exchange_manager_status != Status.RUNNING:
            time.sleep(2)
            self.request_exchange_manager_status()
            Log.d("TM re-requesting EM status")
        self.__status = Status.RUNNING
        Log.d(f"TradingManager is {self.__status.name}.")
        while Status.RUNNING:
            # Use this as a rudimentary switch for testing
            if DEV_TEST_MODE:
                # Loop buying some stocks for test purposes
                time.sleep(6)
                order_list = ["TSLA", "AAPL", "AMZN"]
                x = random.randrange(3)
                asset = Asset(order_list[x], AssetType.PAPER_STOCK)
                asset.trade_intent = TradeIntent.SHORT_TRADE
                order = Order(OrderType.BUY, asset)
                Log.d(f"request allowance for {asset.name}")
                dispatcher.send(request_type=RequestType.ALLOWANCE, order=order, signal=self.__signal.value,
                                sender=self.__sender.value)
            else:
                if self.__assets is None or len(self.__assets) == 0 or not self.__owned_assets_already_inspected:
                    asset: Asset = find_new_asset()
                    if asset is not None:
                        confidence: float = analyse_asset(asset)
                        order_type: OrderType = determine_buy_or_sell(confidence, asset)
                        if order_type == OrderType.BUY or order_type == OrderType.SELL:
                            # we send a request for an allowance to the EM here, then on response of the allowance,
                            # we send an order request.
                            dispatcher.send(request_type=RequestType.ALLOWANCE, order_type=order_type, asset=asset,
                                            signal=self.__signal.value, sender=self.__sender.value)

    def is_running(self) -> bool:
        """
        Determines whether the manager is running.
        :return: running status
        """
        return self.__status == Status.RUNNING

    def is_idle(self) -> bool:
        """
        Determines whether the manager is running.
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

    def request_exchange_manager_status(self):
        """
        Requests the status of the exchange manager.
        """
        dispatcher.send(request_type=RequestType.STATUS, signal=self.__signal.value, sender=self.__sender.value)

    def __dispatcher_receive_order_response(self, status: ResponseStatus, order: Order):
        """
        Called when we receive an order request from the Exchange Manager.  We then process the ResponseType and append
        the Asset to the owned assets list. \n
        :param status: the status of the request made previously by the trade manager.  This should really only be
        successful.
        :param order: the order we requested.
        """
        if status == ResponseStatus.SUCCESSFUL:
            # on success, add to the owned assets if the order status is queued.
            Log.d(f"TradingManager.__dispatcher_receive_order the order for {order.asset.name} is {order.status.name}")
            if order.status == OrderStatus.PROCESSING or order.status == OrderStatus.FILLED:
                return
            if self.__assets is None:
                self.__assets = List[order.asset]
            else:
                self.__assets.append(order.asset)

        elif status == ResponseStatus.UNSUCCESSFUL:
            Log.w(f'Received confirmation that the order was: {status.value}')
            # TODO - what do we want to do if the purchase was unsuccessful?  Do we need more info?
            pass
        elif status == ResponseStatus.MARKET_CLOSED:
            # TODO - should the TM decide whether to resend it, or should the decision be FINAL until completed?
            Log.w(f'Received confirmation that the order was: {status.value}')
            pass

    def __dispatcher_receive_assets_response(self, status: ResponseStatus, assets: List[Asset]):
        """
        Called when we receive an assets' response from the Exchange Manager.  We then process the ResponseType and
        update the owned assets list. \n
        :param status: the status of the request made previously by the trade manager.  This should really only be
        successful.
        :param assets: the assets we currently own.  Note, this doesn't include open orders.
        """
        if status == ResponseStatus.SUCCESSFUL:
            # on success, add to the owned assets.
            if assets is not None:
                self.__assets = assets
        elif status == ResponseStatus.UNSUCCESSFUL:
            # TODO - what do we want to do if the request was unsuccessful?  Do we need more info?
            pass

    def __dispatcher_receive_allowance_response(self, status: ResponseStatus, order: Order):
        """
        Called when we receive an allowance response from the Exchange Manager.  We then process the ResponseType and
        create an order based on the allotted funds. \n
        :param status: the status of the request made previously by the trade manager.  This should really only be
        successful.
        """
        if status == ResponseStatus.SUCCESSFUL:
            # on success, request an order.
            dispatcher.send(request_type=RequestType.TRADE, order=order, signal=self.__signal.value,
                            sender=self.__sender.value)
        elif status == ResponseStatus.UNSUCCESSFUL:
            # TODO - what do we want to do if the request was unsuccessful?  Do we need more info?
            #  Do we want to sell off?
            Log.w(f"TradingManager.__dispatcher_receive_allowance has been unsuccessful for {order.asset.name} "
                  f"valued at {order.asset.value}")
            pass
        elif status == ResponseStatus.DENIED:
            # maybe this is worth considering...
            pass

    def __dispatcher_receive_status_request(self):
        """
        Called when the Exchange Manager requests our status.
        """
        dispatcher.send(response_type=ResponseType.STATUS, manager_status=self.__status, signal=self.__signal.value,
                        sender=self.__sender.value)

    def __dispatcher_receive_status_response(self, status: Status):
        """
        Called when we receive a response from the Exchange Manager status request.
        """

        self.__exchange_manager_status = status

    def __dispatcher_receive(self, status, **kwargs):
        """
        handle dispatcher response.  This is used to communicate with the other Managers.
        :param status: the status of the request
        """
        request_type: RequestType = kwargs.get("request_type")
        response_type: ResponseType = kwargs.get("response_type")
        if request_type is not None:
            if request_type == RequestType.STATUS:
                self.__dispatcher_receive_status_request()
        elif response_type is not None:
            if response_type == ResponseType.TRADE:
                self.__dispatcher_receive_order_response(status, kwargs.get("order"))
            elif response_type == ResponseType.HOLDINGS:
                self.__dispatcher_receive_assets_response(status, kwargs.get("holdings"))
            elif response_type == ResponseType.ALLOWANCE:
                self.__dispatcher_receive_allowance_response(status, kwargs.get("order"))
            elif response_type == ResponseType.STATUS:
                self.__dispatcher_receive_status_response(kwargs.get("manager_status"))
        else:
            Log.e(f"TM.__dispatcher_receive received a bad request/response. both are none.")

    def __owned_assets_already_inspected(self) -> bool:
        """
        check all owned assets have been inspected before we try and find new ones.
        :returns: whether we have already inspected our current asset list.
        """
        if self.__assets is None:
            Log.d(f"TradingManager.__owned_assets_already_inspected: no owned assets.")
            return True
        for asset in self.__assets:
            # if any of the assets haven't been updated in the last little while, return false.
            time_difference = asset.last_updated - datetime.datetime.now()
            if time_difference.total_seconds() > 3600:
                return False
        return True

    def __get_owned_assets(self):
        """
        Sends a request to the Exchange Manager to return all assets we own.
        """
        dispatcher.send(request_type=RequestType.HOLDINGS, signal=self.__signal.value, sender=self.__sender.value)
