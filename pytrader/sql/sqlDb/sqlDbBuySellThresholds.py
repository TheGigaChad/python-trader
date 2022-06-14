from pytrader.sql.sqlDb.sqlDb import SQLDb, SQLDbType


class SQLDbBuySellThresholds(SQLDb):

    def __init__(self):
        super().__init__(SQLDbType.BUY_SELL_THRESHOLDS)
        self.__column_name: str = ""
