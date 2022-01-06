import enum
from pytrader.riskParity.riskParityAsset import RiskParityAsset
from pytrader.exchange.exchangeManager import ExchangeManager
from pytrader.trade.tradingManager import TradingManager


class Status(enum.Enum):
    """
    Enum representing the running state for the manager.
    """
    UNKNOWN = 0
    STARTED = 1
    RUNNING = 2
    ERROR = 3
    STOPPED = 4


class RiskParityManager(TradingManager):
    def __init__(self, exchange_manager: ExchangeManager):
        super().__init__(exchange_manager)

    def start(self):
        pass

    def stop(self):
        pass

    def init(self):
        pass
