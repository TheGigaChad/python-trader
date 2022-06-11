import threading

import pytrader as cfg
from pytrader.SQL.sqlDbManager import SQLDbManager
from pytrader.exchange.exchangeManager import ExchangeManager
from pytrader.models.modelManager import ModelManager
from pytrader.riskParity.riskParityManager import RiskParityManager
from pytrader.trade.tradingManager import TradingManager


def main():
    # Update all SQL data
    sql_manager = SQLDbManager()
    sql_manager.update_local_stores()

    # Update all model data
    model_manager = ModelManager()
    model_manager.load_all()

    # start the managers
    exchange_thread = threading.Thread(target=ExchangeManager)
    exchange_thread.start()
    if cfg.USER_USE_TRADER:
        trade_thread = threading.Thread(target=TradingManager)
        trade_thread.start()
    if cfg.USER_USE_RISK_PARITY:
        risk_parity_thread = threading.Thread(target=RiskParityManager)
        risk_parity_thread.start()


if __name__ == "__main__":
    main()
