from pytrader.riskParity.riskParityManager import RiskParityManager
from pytrader.exchange.exchangeManager import ExchangeManager
from pytrader.trade.tradingManager import TradingManager
from pytrader.config import USER_USE_RISK_PARITY, USER_USE_TRADER


def load_models():
    pass


def load_sql():
    pass


if __name__ == "__main__":
    # load data from online sources
    load_models()
    load_sql()

    # start the managers
    exchange_manager = ExchangeManager()
    managers = []
    if USER_USE_RISK_PARITY:
        risk_parity_manager = RiskParityManager(exchange_manager=exchange_manager)
        managers.append(risk_parity_manager)
    if USER_USE_TRADER:
        trading_manager = TradingManager(exchange_manager=exchange_manager)
        managers.append(trading_manager)





