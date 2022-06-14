import datetime

import pytrader.sql.sqlDb as sqlDb


class SQLManager:
    """
    Holds all sql databases and makes querying easier.
    """

    def __init__(self):
        self.__last_updated: datetime.datetime = datetime.datetime.min
        self.__windowDb: sqlDb.sqlDbWindows = sqlDb.SQLDbWindows()
        self.__buySellThresholdDb: sqlDb.sqlDbBuySellThresholds = sqlDb.sqlDbBuySellThresholds.SQLDbBuySellThresholds()
        self.__tradesDb: sqlDb.sqlDbTrades = sqlDb.sqlDbTrades.SQLDbTrades()
        self.__openTradesDb: sqlDb.sqlDbOpenTrades = sqlDb.sqlDbOpenTrades.SQLDbOpenTrades()

    @property
    def window_db(self):
        return self.__windowDb

    @property
    def buy_sell_threshold_db(self):
        return self.__buySellThresholdDb

    @property
    def trades_db(self):
        return self.__tradesDb

    @property
    def open_trades_db(self):
        return self.__openTradesDb

    @property
    def last_updated(self):
        return self.__last_updated

    def update_local_stores(self):
        """
        Updates local stored sql data to be used for reference later
        """
        self.__windowDb.update_local_stores()
        self.__last_updated = datetime.datetime.now()
