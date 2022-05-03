from pytrader.SQL.sqlDb.sqlDb import SQLDb, SQLDbType


class SQLDbWindows(SQLDb):
    super().__init__(SQLDbType.WINDOW)
