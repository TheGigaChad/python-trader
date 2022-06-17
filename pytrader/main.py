import threading

from pytrader import config, exchange, models, riskParity, sql, trade


def main():
    # Update all sql data
    sql_manager = sql.SQLManager()
    sql_manager.update_local_stores()

    # Update all model data
    model_manager = models.ModelManager()
    model_manager.load_all()

    # start the managers
    exchange_thread = threading.Thread(target=exchange.ExchangeManager)
    exchange_thread.start()

    if config.USER_USE_TRADER:
        trade_thread = threading.Thread(target=trade.TradingManager)
        trade_thread.start()
    if config.USER_USE_RISK_PARITY:
        risk_parity_thread = threading.Thread(target=riskParity.RiskParityManager)
        risk_parity_thread.start()


if __name__ == "__main__":
    main()
