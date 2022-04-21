import datetime
import random
import time
from typing import Optional

from pydispatch import dispatcher

from pytrader.SQL.sqlDb.sqlDb import SQLDb, SQLDbType
from pytrader.common.asset import Asset, AssetType
from pytrader.common.dispatch import Sender, Signal
from pytrader.common.order import Order
from pytrader.common.requests import RequestType, ResponseType
from pytrader.common.status import Status
from pytrader.config import DEV_TEST_MODE


def getOwnedAssets() -> [Asset]:
    """
    return ALL assets from all exchanges
    """
    # TODO - getOwnedAssets() logic
    pass


def determineBuySell(confidence: float, asset: Asset) -> bool:
    """
    determines whether we should buy, sell or ignore the asset based on the confidence value.
    :param confidence: float value relating to how good of a trade is available.
    :param asset: the asset we are inspecting.
    :return: boolean for whether we should buy/sell or ignore
    """
    buy_threshold, sell_threshold = determineBuySellThresholdValues(asset.name)
    buy_sell: bool = False
    if confidence >= buy_threshold:
        buy_sell = True
    return buy_sell


def determineBuySellThresholdValues(asset_name: Asset.name) -> tuple[float, float]:
    """
    return the buy and sell threshold values for the relevant asset.
    :param asset_name: the asset name we are inspecting.
    :return: buy/sell threshold values as tuple.  Buy is first, second is sell.
    """
    # TODO-Tidy - this should use a method to match names...
    db: SQLDb = SQLDb(SQLDbType.BUY_SELL_THRESHOLDS)
    rows, headers = db.runSQLQuery(f"SELECT buy, sell FROM {db.table_name} WHERE name = '{asset_name}';")
    if len(rows) != 1:
        print(f"tradingManager.determineBuySellThresholdValues - no db entry for {asset_name}. creating now...")
        val_a, val_b = db.runSQLQuery(
            f"INSERT INTO {db.table_name} (`name`, `buy`, `sell`, `last_updated`) VALUES ('{asset_name}',"
            f"'1.0','-1.0','{datetime.datetime.now()}');")
        rows, headers = db.runSQLQuery(f"SELECT buy, sell FROM {db.table_name} WHERE name = '{asset_name}';")

    return rows[0][0], rows[0][1]


def analyseAsset(asset: Asset) -> float:
    """
    Processes the asset based on in-built methodologies in order to determine the confidence value of the stock.
    A high value will constitute a purchase opportunity, a low value will mean a sell opportunity.
    :param asset: asset to be analysed.
    :return: confidence value.
    """
    # TODO - analyseAsset() logic
    return random.Random.randrange(-10, 10, 0.01)


def findNewAsset() -> Asset:
    """
    returns a new asset that will be used for inspection for buy/sell opportunities.
    """
    # TODO - create findNewAsset() logic
    return Asset("TSLA", AssetType.PAPER_STOCK)


def calculateQuantity(asset: Asset, confidence: float) -> float:
    """
    creturns the quantity of stocks for the order. \n
    :param confidence: float value relating to how good of a trade is available. (low = sell, buy = high)
    :param asset: the asset we are inspecting.
    :return: how many stocks
    """
    # TODO - calculateQuantity() logic

    return 1.0


def createOrder(asset: Asset, confidence: float) -> Order:
    """
    create an order for the asset based on the confidence value. \n
    :param confidence: float value relating to how good of a trade is available. (low = sell, buy = high)
    :param asset: the asset we are inspecting.
    :return: boolean for whether we should buy/sell or ignore
    """
    # TODO - createOrder() logic - we should look at our db to see buy/sell threshold
    buy_threshold, sell_threshold = determineBuySell()
    request_type: RequestType = RequestType.SELL
    if confidence >= 0.0:
        request_type = RequestType.BUY
    elif confidence < 0:
        request_type = RequestType.SELL
    return Order(request_type=request_type, asset=asset, qty=calculateQuantity(asset, confidence))


class TradingManager:
    """
    The manager that will handle all the threads \n
    """

    def __init__(self):
        self.__threads = None
        self.__status = Status.STARTING
        self.__assets: [Asset] = None
        self.__sender: Sender = Sender.TRADE_MANAGER
        self.__signal: Signal = Signal.TRADE_MANAGER
        self.start()

    @property
    def status(self):
        return self.__status

    def start(self):
        """
        Starts the dispatcher to the exchange manager.
        """
        print("TM STARTING")
        dispatcher.connect(self.__dispatcher_receive, signal=Signal.EXCHANGE_MANAGER.value,
                           sender=Signal.EXCHANGE_MANAGER.value)

        # TODO - probe ALL exchanges for asset list
        self.__assets = getOwnedAssets()
        self.__status = Status.RUNNING
        while 1:
            # Use this as a rudimentary switch for testing
            if DEV_TEST_MODE:
                # Loop buying TSLA for test purposes
                time.sleep(15)
                asset = Asset("TSLA", AssetType.PAPER_STOCK)
                order = Order(request_type=RequestType.BUY, asset=asset, qty=1)
                dispatcher.send(message=order, signal=self.__signal.value, sender=self.__sender.value)
            else:
                if len(self.__assets) == 0 or not self.__ownedAssetsInspected:
                    asset: Asset = findNewAsset()
                    if asset is not None:
                        confidence: float = analyseAsset(asset)
                        if determineBuySell(confidence, asset):
                            order: Order = createOrder(asset=asset, confidence=confidence)
                            dispatcher.send(message=order, signal=self.__signal.value, sender=self.__sender.value)

    def isRunning(self):
        return self.__status == Status.RUNNING

    def isIdle(self):
        return self.__status == Status.IDLE

    def isError(self):
        return self.__status == Status.ERROR

    def isStopped(self):
        return self.__status == Status.STOPPED

    def getAssets(self, asset_type: Optional[AssetType] = AssetType.UNKNOWN) -> list[Asset]:
        """
        returns specified assets as a list.  See ExchangeManager.getAssets for more info. \n
        :param asset_type: asset type if specifically needed, else will return all.
        :return: list of all Assets.
        """
        # return self.__exchange_manager.getAssets(asset_type=asset_type)

    def __dispatcher_receive(self, message):
        """
        handle dispatcher response.  This is used to communicate with the other Managers.
        """
        # TODO - TM should interpret all responses

        if isinstance(message, ResponseType):
            print(f'TM has received message that the order was: {message.value}')

    def __ownedAssetsInspected(self):
        """
        check all owned assets have been inspected before we try and find new ones.
        """
        # TODO - checkOwnedAssets() logic
        return False
