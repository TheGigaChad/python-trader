from pytrader.exchange.exchangeManager import ExchangeManager
from pytrader.common.status import Status


class TradingManager:
    """
    The manager that will handle all the threads
    """
    def __init__(self, exchange_manager: ExchangeManager):
        self.__exchange_manager = exchange_manager
        self.__threads = None
        self.__status = Status.STARTING

    def start(self):
        pass
