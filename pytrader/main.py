import threading

from pytrader.riskParity.riskParityAsset import RiskParityAsset
from pytrader.riskParity.riskParityManager import RiskParityManager
from pytrader.exchange.exchangeManager import ExchangeManager
from pytrader.exchange.exchange import RequestType
from pytrader.common.asset import Asset, AssetType
from pytrader.trade.tradingManager import TradingManager
from pytrader.SQL.sqlDbManager import SQLDbManager
from pytrader.config import USER_USE_RISK_PARITY, USER_USE_TRADER

def load_models():
    pass


def load_sql():
    pass


if __name__ == "__main__":
    # Update all SQL data
    sql_manager = SQLDbManager()
    sql_manager.updateLocalStores()


    # initalise the exchange manager

    exch_thread = threading.Thread(target=ExchangeManager)
    exch_thread.start()

    # asset = Asset("TSLA", AssetType.STOCK)
    # rpa = RiskParityAsset("RPA", AssetType.STOCK)
    # # initialise the risk parity manager
    # risk_parity_manager = RiskParityManager(exchange_manager=exchange_manager)
    # # initialise the trading manager
    # trading_manager = TradingManager(exchange_manager=exchange_manager)
    # trading_manager.request(asset=asset, request_type=ExchangeRequestType.INFO)
    # risk_parity_manager.request(asset=rpa, request_type=ExchangeRequestType.INFO)

    # managers = []
    # if USER_USE_RISK_PARITY:
    #     risk_parity_manager = RiskParityManager(exchange_manager=exchange_manager)
    #     managers.append(risk_parity_manager)
    # if USER_USE_TRADER:
    #     trading_manager = TradingManager(exchange_manager=exchange_manager)
    #     managers.append(trading_manager)
    #




