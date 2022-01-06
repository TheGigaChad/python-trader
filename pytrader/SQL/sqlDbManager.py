from pytrader.config import SQL_SERVER_DATABASE, SQL_SERVER_HOST, SQL_SERVER_USER, SQL_SERVER_PASSWORD, \
    SQL_SERVER_WINDOWS_TABLE

from pytrader.SQL.sqlDb import SQLDb, SQLDbType


class SQLDbManager:
    def __init__(self):
        self.__paper_windowDb = SQLDb(SQLDbType.WINDOW)

