import threading

from pytrader.SQL.sqlDbManager import SQLDbManager
from pytrader.config import USER_USE_RISK_PARITY, USER_USE_TRADER
from pytrader.exchange.exchangeManager import ExchangeManager
from pytrader.models.modelManager import ModelManager
from pytrader.riskParity.riskParityManager import RiskParityManager
from pytrader.trade.tradingManager import TradingManager


def main():
    # Update all SQL data
    sql_manager = SQLDbManager()
    sql_manager.updateLocalStores()

    # Update all model data
    model_manager = ModelManager()
    model_manager.load()

    # start the managers
    exchange_thread = threading.Thread(target=ExchangeManager)
    exchange_thread.start()
    if USER_USE_TRADER:
        trade_thread = threading.Thread(target=TradingManager)
        trade_thread.start()
    if USER_USE_RISK_PARITY:
        risk_parity_thread = threading.Thread(target=RiskParityManager)
        risk_parity_thread.start()


if __name__ == "__main__":
    main()



