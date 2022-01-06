from pytrader.config import SQL_SERVER_DATABASE, SQL_SERVER_HOST, SQL_SERVER_USER, SQL_SERVER_PASSWORD, \
    SQL_SERVER_WINDOWS_TABLE
import enum


class SQLDbType(enum.Enum):
    USERS  = 0
    WINDOW = 1


class SQLDb:
    def __init__(self, db_type: SQLDbType):
        self.__db_type = db_type
        self.__db_name = self.__get_name()

    def __get_name(self):
        if self.__db_type == SQLDbType.WINDOW:
            return SQL_SERVER_WINDOWS_TABLE

