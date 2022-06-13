import datetime

from pytrader.SQL.sqlDb import sqlDbWindows, sqlDbBuySellThresholds, sqlDbTrades, sqlDbOpenTrades


class SQLDbManager:
    """
    Holds all SQL databases and makes querying easier.
    """

    def __init__(self):
        self.__last_updated: datetime.datetime = datetime.datetime.min
        self.__windowDb: sqlDbWindows = sqlDbWindows.SQLDbWindows()
        self.__buySellThresholdDb: sqlDbBuySellThresholds = sqlDbBuySellThresholds.SQLDbBuySellThresholds()
        self.__tradesDb: sqlDbTrades = sqlDbTrades.SQLDbTrades()
        self.__openTradesDb: sqlDbOpenTrades = sqlDbOpenTrades.SQLDbOpenTrades()

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
        Updates local stored SQL data to be used for reference later
        """
        self.__windowDb.update_local_stores()
        self.__last_updated = datetime.datetime.now()
