import datetime
from typing import Optional

from pytrader.SQL.sqlDb.Daos.sqlDbTradesDao import SQLDbTradesDao
from pytrader.SQL.sqlDb.sqlDb import SQLDb, SQLDbType, SQLQueryResponseType
from pytrader.common.requests import ResponseType, RequestType
from pytrader.config import SQL_SERVER_TRADES_TABLE_COLUMN_NAME, SQL_SERVER_TRADES_TABLE_COLUMN_ORDER_TYPE, \
    SQL_SERVER_TRADES_TABLE_COLUMN_ORDER_ID, SQL_SERVER_TRADES_TABLE_COLUMN_EXCHANGE, \
    SQL_SERVER_TRADES_TABLE_COLUMN_QUANTITY, SQL_SERVER_TRADES_TABLE_COLUMN_TIMESTAMP


class SQLDbTrades(SQLDb):
    """
    the sql db class that relates to the Trades db.
    """

    def __init__(self):
        super().__init__(SQLDbType.TRADES)
        self.__column_name: str = SQL_SERVER_TRADES_TABLE_COLUMN_NAME
        self.__column_order_type: str = SQL_SERVER_TRADES_TABLE_COLUMN_ORDER_TYPE
        self.__column_quantity: str = SQL_SERVER_TRADES_TABLE_COLUMN_QUANTITY
        self.__column_order_id: str = SQL_SERVER_TRADES_TABLE_COLUMN_ORDER_ID
        self.__column_timestamp: str = SQL_SERVER_TRADES_TABLE_COLUMN_TIMESTAMP
        self.__column_exchange: str = SQL_SERVER_TRADES_TABLE_COLUMN_EXCHANGE

    @property
    def column_order_id(self):
        return self.__column_order_id.strip('`')

    @property
    def column_order_type(self):
        return self.__column_order_type.strip('`')

    def __create_dao(self, rows) -> SQLDbTradesDao:
        """
        helper function to create a SQLDbTradesDao object
        @param rows: a list of rows holding the data
        @return: SQLDbTradesDao object
        """
        return SQLDbTradesDao(rows[0], rows[1], rows[2], rows[3], rows[4], rows[5])

    def get_trade_by_order_id(self, order_id: int) -> Optional[SQLDbTradesDao]:
        """
        gets a specific trade from the SQL server by the order id. \n
        :param order_id: the id of the trade.
        """
        query = f"SELECT * FROM `{super().table_name}` WHERE {self.__column_order_id} = {order_id}"
        rows, columns = self.run_sql_query(query)
        if len(rows) == 0:
            return None
        return self.__create_dao(rows[0])

    def get_trade_by_timestamp(self, timestamp: datetime.datetime) -> SQLDbTradesDao:
        """
        gets a specific trade from the SQL server by the timestamp. if multiple exist, will return first instance. \n
        :param timestamp: the datetime of the trade.
        """
        query = f"SELECT * FROM `{super().table_name}` WHERE {self.__column_timestamp} = {timestamp}"
        rows, columns = self.run_sql_query(query)
        return self.__create_dao(rows[0])

    def get_all_trades(self) -> [SQLDbTradesDao]:
        """
        gets all trades from the SQL server.
        """
        query = f"SELECT * FROM `{super().table_name}` WHERE 1"
        rows, columns = self.run_sql_query(query)
        trade_list: list = []
        if rows is None or columns is None:
            return trade_list

        if len(rows) == 0:
            return trade_list

        for trade in rows:
            trade_list.append(self.__create_dao(trade))
        return trade_list

    def get_all_buy_trades(self) -> [SQLDbTradesDao]:
        """
        gets all buy trades from the SQL server.
        """
        query = f"SELECT * FROM `{super().table_name}` WHERE {self.__column_order_type} = '{RequestType.BUY.name}'"
        rows, columns = self.run_sql_query(query)
        trade_list: list = []
        if rows is None or columns is None:
            return trade_list

        if len(rows) == 0:
            return trade_list

        for trade in rows:
            trade_list.append(self.__create_dao(trade))
        return trade_list

    def get_all_sell_trades(self) -> [SQLDbTradesDao]:
        """
        gets all sell trades from the SQL server.
        """
        query = f"SELECT * FROM `{super().table_name}` WHERE {self.column_order_type} = '{RequestType.SELL.name}';"
        rows, columns = self.run_sql_query(query)
        trade_list: list = []
        if rows is None or columns is None:
            return trade_list

        if len(rows) == 0:
            return trade_list

        for trade in rows:
            trade_list.append(self.__create_dao(trade))
        return trade_list

    def commit_trade(self, dao: SQLDbTradesDao) -> SQLQueryResponseType:
        """
        commits a trade dao into the db. \n
        :param dao: trade object being sent to db
        :return: whether the commit was successful or not
        """
        query = f"INSERT INTO `{super().table_name}` ({self.__column_name}, {self.__column_order_type}, " \
                  f"{self.__column_quantity}, {self.__column_order_id}, {self.__column_timestamp}, {self.__column_exchange}) " \
                  f"VALUES (%s, %s, %s, %s, %s, %s);"
        params = (dao.name,
                  dao.order_type.name.__str__(), dao.quantity.__str__(), dao.order_id.__str__(), dao.timestamp.__str__(),
                  dao.exchange.name.__str__())
        return self.runSQLQueryNoResponse(query, params)

    def delete_trade(self, dao: SQLDbTradesDao) -> SQLQueryResponseType:
        """
        deletes trade from db.  Should only be used for testing and helper functions.  There is no need to delete
        records... \n
        :param dao: trade to be deleted
        :return: whether the deletion was successful
        """
        query = f"DELETE FROM {super().table_name} WHERE {self.column_order_id} = %s;"
        params = [dao.order_id]
        return self.runSQLQueryNoResponse(query, params)

    def is_order_id_unique(self, order_id: int) -> bool:
        """
        determines whether the order id exists in the db.  this is used to ensure the order id is unique. \n
        :param order_id: id of the order
        :return: whether the order id exist in db
        """
        query = f"SELECT * FROM `{super().table_name}` WHERE {self.__column_order_id} = {order_id}"
        rows, columns = self.run_sql_query(query)
        if rows is None and columns is not None:
            return True
        else:
            return False
