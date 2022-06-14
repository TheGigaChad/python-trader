from pytrader.sql.sqlDb.sqlDb import SQLDb, SQLDbType


class SQLDbWindows(SQLDb):
    def __init__(self):
        super().__init__(SQLDbType.WINDOW)
        self.__column_name: str = ""
