import datetime
import random
import time
from typing import Optional, List

from pydispatch import dispatcher

from pytrader import common, config

Log = common.Log(__file__)


def determine_buy_or_sell(confidence: float, buy_threshold: float, sell_threshold: float) -> Optional[common.OrderType]:
    """
    determines whether we should buy, sell or ignore the asset based on the confidence value.
    :param confidence: float value relating to how good of a trade is available.
    :param sell_threshold: the confidence level we determine that a good sale point is.
    :param buy_threshold: the confidence level we determine that a good buy point is.
    :return: order type or None if nothing is a good idea.
    """
    if confidence >= buy_threshold:
        return common.OrderType.BUY
    elif confidence <= sell_threshold:
        return common.OrderType.SELL
    else:
        return None


def analyse_asset(asset: common.Asset) -> float:
    """
    Processes the asset based on in-built methodologies in order to determine the confidence value of the stock.
    A high value will constitute a purchase opportunity, a low value will mean a sell opportunity.
    :param asset: asset to be analysed.
    :return: confidence value.
    """
    # TODO - analyseAsset() logic
    return random.randrange(-10, 10, 1) + random.random()


def find_new_asset() -> common.Asset:
    """
    returns a new asset that will be used for inspection for buy/sell opportunities.
    """
    # TODO - create findNewAsset() logic
    return common.Asset("TSLA", common.AssetType.PAPER_STOCK)


class TradingManager:
    """
    The manager that will handle all the trading based on predetermined models.  It will also look for new potential
    trades.
    """

    def __init__(self):
        self.__threads = None
        self.__status = common.State.STARTING
        self.__assets: Optional[List[common.Asset]] = None
        self.__sender: common.Sender = common.Sender.TRADE_MANAGER
        self.__signal: common.Signal = common.Signal.TRADE_MANAGER
        self.__exchange_manager_status: common.State = common.State.UNKNOWN
        self.start()

    @property
    def status(self):
        return self.__status

    def start(self):
        """
        Starts the dispatcher to the exchange manager.
        """
        Log.d("TradingManager is starting.")
        dispatcher.connect(self.__dispatcher_receive, signal=common.Signal.EXCHANGE_MANAGER.value,
                           sender=common.Signal.EXCHANGE_MANAGER.value)

        # TODO - probe ALL exchanges for asset list
        self.__status = common.State.STARTING
        Log.d("TradingManager is waiting on Exchange Manager for the list of owned assets.")
        while self.__assets is None:
            # wait for the list of owned assets.
            time.sleep(3)
            self.__get_owned_assets()
        self.__status = common.State.READY
        while self.__exchange_manager_status != common.State.RUNNING:
            time.sleep(2)
            self.request_exchange_manager_status()
            Log.d("TM re-requesting EM status")
        self.__status = common.State.RUNNING
        Log.d(f"TradingManager is {self.__status.name}.")
        while common.State.RUNNING:
            # Use this as a rudimentary switch for testing
            # TODO - remove this crapola
            if config.DEV_TEST_MODE:
                # Loop buying some stocks for test purposes
                time.sleep(6)
                order_list = ["TSLA", "AAPL", "AMZN"]
                x = random.randrange(3)
                asset = common.Asset(order_list[x], common.AssetType.PAPER_STOCK)
                asset.trade_intent = common.TradeIntent.SHORT_TRADE
                self.__request_asset_thresholds(asset)
            else:
                if self.__assets is None or len(self.__assets) == 0 or not self.__owned_assets_already_inspected:
                    asset: common.Asset = find_new_asset()
                    if asset is not None:
                        self.__request_asset_thresholds(asset)

    def is_running(self) -> bool:
        """
        Determines whether the manager is running.
        :return: running status
        """
        return self.__status == common.State.RUNNING

    def is_idle(self) -> bool:
        """
        Determines whether the manager is running.
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

    def request_exchange_manager_status(self):
        """
        Requests the status of the exchange manager.
        """
        dispatcher.send(request_type=common.RequestType.STATUS, signal=self.__signal.value, sender=self.__sender.value)

    def __request_asset_thresholds(self, asset: common.Asset):
        """
        requests the buy and sell thresholds for the given asset.
        :param asset: asset being evaluated.
        """
        dispatcher.send(request_type=common.RequestType.BUY_SELL_THRESHOLDS, asset=asset,
                        signal=self.__signal.value, sender=self.__sender.value)

    def __dispatcher_receive_order_response(self, status: common.ResponseStatus, order: common.Order):
        """
        Called when we receive an order request from the Exchange Manager.  We then process the ResponseType and append
        the Asset to the owned assets list. \n
        :param status: the status of the request made previously by the trade manager.  This should really only be
        successful.
        :param order: the order we requested.
        """
        if status == common.ResponseStatus.SUCCESSFUL:
            # on success, add to the owned assets if the order status is queued.
            Log.d(f"TradingManager.__dispatcher_receive_order the order for {order.asset.name} is {order.status.name}")
            if order.status == common.OrderStatus.PROCESSING or order.status == common.OrderStatus.FILLED:
                return
            if self.__assets is None:
                self.__assets = List[order.asset]
            else:
                self.__assets.append(order.asset)

        elif status == common.ResponseStatus.UNSUCCESSFUL:
            Log.w(f'Received confirmation that the order was: {status.value}')
            # TODO - what do we want to do if the purchase was unsuccessful?  Do we need more info?
            pass
        elif status == common.ResponseStatus.MARKET_CLOSED:
            # TODO - should the TM decide whether to resend it, or should the decision be FINAL until completed?
            Log.w(f'Received confirmation that the order was: {status.value}')
            pass

    def __dispatcher_receive_assets_response(self, status: common.ResponseStatus, assets: List[common.Asset]):
        """
        Called when we receive an assets' response from the Exchange Manager.  We then process the ResponseType and
        update the owned assets list. \n
        :param status: the status of the request made previously by the trade manager.  This should really only be
        successful.
        :param assets: the assets we currently own.  Note, this doesn't include open orders.
        """
        if status == common.ResponseStatus.SUCCESSFUL:
            # on success, add to the owned assets.
            if assets is not None:
                self.__assets = assets
        elif status == common.ResponseStatus.UNSUCCESSFUL:
            # TODO - what do we want to do if the request was unsuccessful?  Do we need more info?
            pass

    def __dispatcher_receive_allowance_response(self, status: common.ResponseStatus, order: common.Order):
        """
        Called when we receive an allowance response from the Exchange Manager.  We then process the ResponseType and
        create an order based on the allotted funds. \n
        :param status: the status of the request made previously by the trade manager.  This should really only be
        successful.
        """
        if status == common.ResponseStatus.SUCCESSFUL:
            # on success, request an order.
            dispatcher.send(request_type=common.RequestType.TRADE, order=order, signal=self.__signal.value,
                            sender=self.__sender.value)
        elif status == common.ResponseStatus.UNSUCCESSFUL:
            # TODO - what do we want to do if the request was unsuccessful?  Do we need more info?
            #  Do we want to sell off?
            Log.w(f"TradingManager.__dispatcher_receive_allowance has been unsuccessful for {order.asset.name} "
                  f"valued at {order.asset.value}")
            pass
        elif status == common.ResponseStatus.DENIED:
            # maybe this is worth considering...
            pass

    def __dispatcher_receive_status_request(self):
        """
        Called when the Exchange Manager requests our status.
        """
        dispatcher.send(response_type=common.ResponseType.STATUS, manager_status=self.__status,
                        signal=self.__signal.value,
                        sender=self.__sender.value)

    def __dispatcher_receive_status_response(self, status: common.State):
        """
        Called when we receive a response from the Exchange Manager status request.
        """

        self.__exchange_manager_status = status

    def __dispatcher_receive_thresholds_response(self, asset: common.Asset, buy_threshold: float,
                                                 sell_threshold: float):
        """
        Called when we receive a response from the Exchange Manager regarding our buy and sell threshold values that
        we will use to determine whether we buy or sell a stock.
        :param asset: asset we are trying to find values for.
        :param buy_threshold: the buy threshold from the SQL table
        :param sell_threshold: the sell threshold from the SQL table
        """
        confidence: float = analyse_asset(asset)
        order_type: common.OrderType = determine_buy_or_sell(confidence, buy_threshold, sell_threshold)
        if order_type == common.OrderType.BUY or order_type == common.OrderType.SELL:
            # we send a request for an allowance to the EM here, then on response of the allowance,
            # we send an order request.
            order: common.Order = common.Order(order_type, asset)
            dispatcher.send(request_type=common.RequestType.ALLOWANCE, order=order,
                            signal=self.__signal.value, sender=self.__sender.value)

    def __dispatcher_receive(self, status, **kwargs):
        """
        handle dispatcher response.  This is used to communicate with the other Managers.
        :param status: the status of the request
        """
        request_type: common.RequestType = kwargs.get("request_type")
        response_type: common.ResponseType = kwargs.get("response_type")
        if request_type is not None:
            if request_type == common.RequestType.STATUS:
                self.__dispatcher_receive_status_request()
        elif response_type is not None:
            if response_type == common.ResponseType.TRADE:
                self.__dispatcher_receive_order_response(status, kwargs.get("order"))
            elif response_type == common.ResponseType.HOLDINGS:
                self.__dispatcher_receive_assets_response(status, kwargs.get("holdings"))
            elif response_type == common.ResponseType.ALLOWANCE:
                self.__dispatcher_receive_allowance_response(status, kwargs.get("order"))
            elif response_type == common.ResponseType.STATUS:
                self.__dispatcher_receive_status_response(kwargs.get("manager_status"))
            elif response_type == common.ResponseType.BUY_SELL_THRESHOLDS:
                self.__dispatcher_receive_thresholds_response(kwargs.get("asset"), kwargs.get("buy_threshold"),
                                                              kwargs.get("sell_threshold"))
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
        dispatcher.send(request_type=common.RequestType.HOLDINGS, signal=self.__signal.value,
                        sender=self.__sender.value)
