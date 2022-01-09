import time
from typing import Optional
from pydispatch import dispatcher

from pytrader.common.requests import RequestType, ResponseType
from pytrader.exchange.exchangeManager import ExchangeManager
from pytrader.common.status import Status
from pytrader.common.asset import Asset, AssetType
from pytrader.common.dispatch import Sender, Signal
from pytrader.common.order import Order


class TradingManager:
    """
    The manager that will handle all the threads
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
        self.__status = Status.RUNNING
        while 1:
            time.sleep(15)
            asset = Asset("TSLA", AssetType.PAPER_STOCK)
            order = Order(request_type=RequestType.BUY, asset=asset)
            dispatcher.send(message=order, signal=self.__signal.value, sender=self.__sender.value)

    def isRunning(self):
        return self.__status == Status.RUNNING

    def isIdle(self):
        return self.__status == Status.RUNNING

    def isError(self):
        return self.__status == Status.RUNNING

    def isStopped(self):
        return self.__status == Status.STOPPED

    def getAssets(self, asset_type: Optional[AssetType] = AssetType.UNKNOWN) -> list[Asset]:
        """
        returns specified assets as a list.  See ExchangeManager.getAssets for more info.
        :param asset_type: asset type if specifically needed, else will return all.
        :return: list of all Assets.
        """
        # return self.__exchange_manager.getAssets(asset_type=asset_type)

    def __dispatcher_receive(self, message):
        """
        handle dispatcher response.  This is used to communicate with the other Managers.
        """
        if isinstance(message, ResponseType):
            print(f'TM has received message that the order was: {message.value}')


    
