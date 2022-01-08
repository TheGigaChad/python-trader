import datetime
import json
from typing import Union, Optional

from pytrader.config import SQL_SERVER_DATABASE, SQL_SERVER_HOST, SQL_SERVER_USER, SQL_SERVER_PASSWORD, \
    SQL_SERVER_WINDOWS_TABLE
import mysql.connector as mysql
import enum
from pathlib import Path


def SQLResponseToJson(sql_response: list, column_names: list) -> json:
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


class SQLDb:
    """
    Class that holds all info for a table reference
    """

    def __init__(self, db_type: SQLDbType):
        self.__db_type: SQLDbType = db_type
        self.__db_name: str = self.__get_db_name()
        self.__table_name: str = self.__get_table_name()
        self.__user: str = self.__get_user()
        self.__password: str = self.__get_password()
        self.__host: str = self.__get_host()
        self.__local_dir: Path = self.__get_local_dir()
        self.__last_updated : datetime.datetime = datetime.datetime.min

    @property
    def last_updated(self):
        return self.__last_updated

    def __get_db_name(self) -> str:
        if self.__db_type == SQLDbType.WINDOW:
            return SQL_SERVER_DATABASE

    def __get_table_name(self) -> str:
        if self.__db_type == SQLDbType.WINDOW:
            return SQL_SERVER_WINDOWS_TABLE

    def __get_user(self) -> str:
        if self.__db_type == SQLDbType.WINDOW:
            return SQL_SERVER_USER

    def __get_password(self) -> str:
        if self.__db_type == SQLDbType.WINDOW:
            return SQL_SERVER_PASSWORD

    def __get_host(self) -> str:
        if self.__db_type == SQLDbType.WINDOW:
            return SQL_SERVER_HOST

    def __get_local_dir(self) -> Path:
        local_dir = Path(__file__).parent
        if self.__db_type == SQLDbType.WINDOW:
            return local_dir / 'data/windows.json'

    def runSQLQuery(self, query: str) -> tuple[any, any]:
        """
        Runs a specified query on the db and returns the response and column_names as a tuple
        """
        db_connection = mysql.connect(host=self.__host, database=self.__db_name, user=self.__user,
                                      password=self.__password)
        cursor = db_connection.cursor()
        cursor.execute(query)
        response = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        cursor.close()
        return response, column_names

    def updateLocalStore(self, sql_query: str):
        """
        updates a single local store, with specified query data
        :param sql_query: sql query to be run
        """
        response, column_names = self.runSQLQuery(query=sql_query)
        sql_json = SQLResponseToJson(response, column_names)
        # empty the data
        open(self.__local_dir, 'w').close()

        # write new data
        with open(self.__local_dir, "w") as outfile:
            assert outfile.writable()
            outfile.write(sql_json)
            outfile.close()

    def updateLocalStores(self):
        """
        Updates all local stores related to the db and updates the last_updated time.
        """
        if self.__db_type == SQLDbType.WINDOW:
            sql_query = f"SELECT * FROM {self.__table_name} WHERE 1"
            self.updateLocalStore(sql_query)

        self.__last_updated = datetime.datetime.now()
