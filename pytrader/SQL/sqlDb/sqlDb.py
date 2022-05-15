import datetime
import enum
import json
from pathlib import Path
from typing import Optional, Tuple

import mysql.connector as mysql

import pytrader.cfg as cfg


def sql_response_to_json(sql_response: list, column_names: list) -> json:
    """
    Converts SQL responses to JSON format
    :param sql_response: response data
    :param column_names: names of columns of table
    :return: Json string of data
    """
    sql_data_list = []
    for row in sql_response:
        window_json_item = {}
        for i in range(len(column_names)):
            window_json_item[column_names[i]] = row[i]
        sql_data_list.append(window_json_item)
    return json.dumps(sql_data_list, indent=1)


class SQLDbType(enum.Enum):
    USERS = 0
    WINDOW = 1
    BUY_SELL_THRESHOLDS = 2
    TRADES = 3


class SQLDbQueryType(enum.Enum):
    """
    enum type that specifies the query type for generic requests
    """
    GET_VALUE = 0
    GET_ALL = 1
    INSERT = 2
    DELETE = 3
    UPDATE = 4


class SQLQueryResponseType(enum.Enum):
    """
    enum that represents whether the sql request was successful or not.
    """
    SUCCESSFUL = 0
    UNSUCCESSFUL = 1


class SQLDb:
    """
    Class that holds all info for a table reference
    """

    def __init__(self, db_type: SQLDbType):
        self.__db_type: SQLDbType = db_type
        self.__db_name: str = self.__get_db_name()
        self.__table_name: str = self.table_name
        self.__user: str = self.__get_user()
        self.__password: str = self.__get_password()
        self.__host: str = self.__get_host()
        self.__local_dir: Path = self.__get_local_dir()
        self.__last_updated: datetime.datetime = datetime.datetime.min

    @property
    def last_updated(self):
        return self.__last_updated

    @property
    def table_name(self) -> str:
        if self.__db_type == SQLDbType.WINDOW:
            return cfg.SQL_SERVER_WINDOWS_TABLE
        if self.__db_type == SQLDbType.BUY_SELL_THRESHOLDS:
            return cfg.SQL_SERVER_BUY_SELL_THRESHOLDS_TABLE
        if self.__db_type == SQLDbType.TRADES:
            return cfg.SQL_SERVER_TRADES_TABLE

    def __get_db_name(self) -> str:
        if self.__db_type == SQLDbType.WINDOW or self.__db_type == SQLDbType.BUY_SELL_THRESHOLDS \
                or self.__db_type == SQLDbType.TRADES:
            return cfg.SQL_SERVER_DATABASE

    def __get_user(self) -> str:
        if self.__db_type == SQLDbType.WINDOW or self.__db_type == SQLDbType.BUY_SELL_THRESHOLDS \
                or self.__db_type == SQLDbType.TRADES:
            return cfg.SQL_SERVER_USER

    def __get_password(self) -> str:
        if self.__db_type == SQLDbType.WINDOW or self.__db_type == SQLDbType.BUY_SELL_THRESHOLDS \
                or self.__db_type == SQLDbType.TRADES:
            return cfg.SQL_SERVER_PASSWORD

    def __get_host(self) -> str:
        if self.__db_type == SQLDbType.WINDOW or self.__db_type == SQLDbType.BUY_SELL_THRESHOLDS \
                or self.__db_type == SQLDbType.TRADES:
            return cfg.SQL_SERVER_HOST

    def __get_local_dir(self) -> Path:
        local_dir = Path(__file__).parent
        if self.__db_type == SQLDbType.WINDOW:
            return local_dir / 'data/windows.json'
        elif self.__db_type == SQLDbType.BUY_SELL_THRESHOLDS:
            return local_dir / 'data/buy_sell_thresholds.json'
        elif self.__db_type == SQLDbType.TRADES:
            return local_dir / 'data/trades.json'

    def run_sql_query(self, query: str, expect_output: Optional[bool] = True, params: Optional = None) -> Tuple[any,
                                                                                                                any]:
        """
        Runs a specified query on the db and returns the response and column_names as a tuple
        """
        # TODO - this should be a little more bulletproof
        # default params and setup types
        db_connection = mysql.connect(host=self.__host, database=self.__db_name, user=self.__user,
                                      password=self.__password)
        cursor = db_connection.cursor()
        try:
            cursor.execute(query)
            response = cursor.fetchall()

            if cursor.description is not None:
                column_names = [i[0] for i in cursor.description]
            else:
                column_names = None
            cursor.close()
            return response, column_names
        except Exception as e:
            print(f"sqlDb.runQuery failed. query: {query}, exception: {e}")
            return None, None

    def run_sql_query_no_response(self, query, params) -> SQLQueryResponseType:
        """
        Runs a specified query on the db and returns the response and column_names as a tuple
        """
        # TODO - this should be a little more bulletproof
        # default params and setup types
        db_connection = mysql.connect(host=self.__host, database=self.__db_name, user=self.__user,
                                      password=self.__password)
        cursor = db_connection.cursor()
        try:
            cursor.execute(query, params)
            db_connection.commit()
            return SQLQueryResponseType.SUCCESSFUL
        except Exception as e:
            print(f"sqlDb.runQuery failed. query: {query}, exception: {e}")
            db_connection.rollback()
            return SQLQueryResponseType.UNSUCCESSFUL
        finally:
            db_connection.close()

    def update_local_store(self, sql_query: str):
        """
        updates a single local store, with specified query data
        :param sql_query: sql query to be run
        """
        response, column_names = self.run_sql_query(query=sql_query)
        sql_json = sql_response_to_json(response, column_names)
        # empty the data
        open(self.__local_dir, 'w').close()

        # write new data
        with open(self.__local_dir, "w") as outfile:
            assert outfile.writable()
            outfile.write(sql_json)
            outfile.close()

    def update_local_stores(self):
        """
        Updates all local stores related to the db and updates the last_updated time.
        """
        if self.__db_type == SQLDbType.WINDOW:
            sql_query = f"SELECT * FROM {self.__table_name} WHERE 1"
            self.update_local_store(sql_query)

        if self.__db_type == SQLDbType.BUY_SELL_THRESHOLDS:
            sql_query = f"SELECT * FROM {self.__table_name} WHERE 1"
            self.update_local_store(sql_query)

        self.__last_updated = datetime.datetime.now()
