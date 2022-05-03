import datetime
from pytrader.SQL.sqlDb.sqlDb import SQLDb, SQLDbType


class SQLDbManager:
    """
    Holds all SQL databases and makes querying easier.
    """
    def __init__(self):
        self.__last_updated: datetime.datetime = datetime.datetime.min
        self.__windowDb: SQLDb = SQLDb(SQLDbType.WINDOW)
        self.__buySellThresholdDb: SQLDb = SQLDb(SQLDbType.BUY_SELL_THRESHOLDS)
        self.__tradesDb: SQLDb = SQLDb(SQLDbType.TRADES)

    @property
    def windowDb(self):
        return self.__windowDb

    @property
    def buySellThresholdDb(self):
        return self.__buySellThresholdDb

    @property
    def tradesDb(self):
        return self.__tradesDb

    @property
    def last_updated(self):
        return self.__last_updated

    def updateLocalStores(self):
        """
        Updates local stored SQL data to be used for reference later
        """
        self.__windowDb.updateLocalStores()
        self.__last_updated = datetime.datetime.now()



