from typing import Optional

from pytrader.exchange.exchangeManager import ExchangeManager
from pytrader.common.status import Status
from pytrader.common.asset import Asset, AssetType


class TradingManager:
    """
    The manager that will handle all the threads
    """

    def __init__(self, exchange_manager: ExchangeManager):
        self.__exchange_manager = exchange_manager
        self.__threads = None
        self.__status = Status.STARTING
        self.__assets: [Asset] = None

    @property
    def request(self):
        return self.__exchange_manager.request

    @property
    def status(self):
        return self.__status

    def start(self):
        self.__status = Status.RUNNING

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
        return self.__exchange_manager.getAssets(asset_type=asset_type)

    
