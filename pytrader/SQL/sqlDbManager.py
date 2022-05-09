import datetime

import pytrader.SQL.sqlDb as sqlDb


class SQLDbManager:
    """
    Holds all SQL databases and makes querying easier.
    """

    def __init__(self):
        self.__last_updated: datetime.datetime = datetime.datetime.min
        self.__windowDb: sqlDb.SQLDb = sqlDb.SQLDb(sqlDb.SQLDbType.WINDOW)
        self.__buySellThresholdDb: sqlDb.SQLDb = sqlDb.SQLDb(sqlDb.SQLDbType.BUY_SELL_THRESHOLDS)
        self.__tradesDb: sqlDb.SQLDb = sqlDb.SQLDb(sqlDb.SQLDbType.TRADES)

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
    def last_updated(self):
        return self.__last_updated

    def update_local_stores(self):
        """
        Updates local stored SQL data to be used for reference later
        """
        self.__windowDb.update_local_stores()
        self.__last_updated = datetime.datetime.now()
