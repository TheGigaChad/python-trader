import datetime
import random
from typing import Optional

import pytrader.sql.sqlDb as sqlDb
from pytrader.common.order import Order, OrderType
from pytrader.common.requests import RequestType
from pytrader.config import SQL_SERVER_OPEN_TRADES_COLUMN_NAME, SQL_SERVER_OPEN_TRADES_COLUMN_ORDER_TYPE, \
    SQL_SERVER_OPEN_TRADES_COLUMN_QUANTITY, SQL_SERVER_OPEN_TRADES_COLUMN_TRADE_INTENT, \
    SQL_SERVER_OPEN_TRADES_COLUMN_ORDER_ID, SQL_SERVER_OPEN_TRADES_COLUMN_LAST_UPDATED, \
    SQL_SERVER_OPEN_TRADES_COLUMN_ASSET_TYPE


class SQLDbOpenTrades(sqlDb.SQLDb):
    """
    the sql db class that relates to the Trades db.
    """

    def __init__(self):
        super().__init__(sqlDb.SQLDbType.OPEN_TRADES)
        self.__column_name: str = SQL_SERVER_OPEN_TRADES_COLUMN_NAME
        self.__column_asset_type: str = SQL_SERVER_OPEN_TRADES_COLUMN_ASSET_TYPE
        self.__column_order_type: str = SQL_SERVER_OPEN_TRADES_COLUMN_ORDER_TYPE
        self.__column_trade_intent: str = SQL_SERVER_OPEN_TRADES_COLUMN_TRADE_INTENT
        self.__column_quantity: str = SQL_SERVER_OPEN_TRADES_COLUMN_QUANTITY
        self.__column_order_id: str = SQL_SERVER_OPEN_TRADES_COLUMN_ORDER_ID
        self.__column_timestamp: str = SQL_SERVER_OPEN_TRADES_COLUMN_LAST_UPDATED

    @property
    def column_order_id(self):
        return self.__column_order_id.strip('`')

    @property
    def column_order_type(self):
        return self.__column_order_type.strip('`')

    @staticmethod
    def __create_dao(rows: []) -> sqlDb.daos.SQLDbOpenTradesDao:
        """
        helper function to create a SQLDbTradesDao object
        @param rows: a list of rows holding the data
        @return: SQLDbTradesDao object
        """
        return sqlDb.daos.SQLDbOpenTradesDao(rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6])

    def get_trade_by_order_id(self, order_id: int) -> Optional[sqlDb.daos.SQLDbOpenTradesDao]:
        """
        gets a specific trade from the sql server by the order id. \n
        :param order_id: the id of the trade.
        """
        query = f"SELECT * FROM `{super().table_name}` WHERE {self.__column_order_id} = {order_id}"
        rows, columns = self.run_sql_query(query)
        if len(rows) == 0:
            return None
        return self.__create_dao(rows[0])

    def get_trade_by_timestamp(self, timestamp: datetime.datetime) -> sqlDb.daos.SQLDbOpenTradesDao:
        """
        gets a specific trade from the sql server by the timestamp. if multiple exist, will return first instance. \n
        :param timestamp: the datetime of the trade.
        """
        query = f"SELECT * FROM `{super().table_name}` WHERE {self.__column_timestamp} = {timestamp}"
        rows, columns = self.run_sql_query(query)
        return self.__create_dao(rows[0])

    def get_all_trades(self) -> [sqlDb.daos.SQLDbOpenTradesDao]:
        """
        gets all trades from the sql server.
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

    def get_all_buy_trades(self) -> [sqlDb.daos.SQLDbTradesDao]:
        """
        gets all buy trades from the sql server.
        """
        query = f"SELECT * FROM `{super().table_name}` " \
                f"WHERE {self.__column_order_type} = '{RequestType.BUY.name}' "
        rows, columns = self.run_sql_query(query)
        trade_list: list = []
        if rows is None or columns is None:
            return trade_list

        if len(rows) == 0:
            return trade_list

        for trade in rows:
            trade_list.append(self.__create_dao(trade))
        return trade_list

    def get_all_sell_trades(self) -> [sqlDb.daos.SQLDbTradesDao]:
        """
        gets all sell trades from the sql server.
        """
        query = f"SELECT * FROM `{super().table_name}` " \
                f"WHERE {self.column_order_type} = '{RequestType.SELL.name}';"
        rows, columns = self.run_sql_query(query)
        trade_list: list = []
        if rows is None or columns is None:
            return trade_list

        if len(rows) == 0:
            return trade_list

        for trade in rows:
            trade_list.append(self.__create_dao(trade))
        return trade_list

    def commit_trade(self, order: Order) -> sqlDb.SQLQueryResponseType:
        """
        commits a trade dao into the db. \n
        :param order: trade object being sent to db
        :return: whether the commit was successful or not
        """
        query = f"INSERT INTO `{super().table_name}` ({self.__column_name}, {self.__column_asset_type}, " \
                f"{self.__column_trade_intent}, {self.__column_order_type}, {self.__column_quantity}, " \
                f"{self.__column_order_id}, {self.__column_timestamp}) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        params = (order.asset.name,
                  order.asset.type.name.__str__(), order.asset.trade_intent.name.__str__(), order.type.name.__str__(),
                  order.asset.qty.__str__(), order.asset.id.__str__(), order.asset.last_updated.__str__())
        return self.run_sql_query_no_response(query, params)

    def delete_trade(self, order: Order) -> sqlDb.SQLQueryResponseType:
        """
        deletes trade from db.  Should only be used for testing and helper functions.  There is no need to delete
        records... \n
        :param order: order to be deleted
        :return: whether the deletion was successful
        """
        query = f"DELETE FROM {super().table_name} WHERE {self.column_order_id} = %s;"
        params = [order.asset.id]
        return self.run_sql_query_no_response(query, params)

    def update_trade(self, order: Order) -> sqlDb.SQLQueryResponseType:
        """
        updates order within db with provided order data.
        :param order: order to update
        :return: response from sql query.
        """
        query = f"UPDATE `{super().table_name}` " \
                f"SET {self.__column_quantity} = %s, {self.__column_timestamp} = %s " \
                f"WHERE {self.__column_order_id} = %s;"
        params = (order.asset.qty.__str__(), order.asset.last_updated.__str__(), order.asset.id.__str__())

        return self.run_sql_query_no_response(query, params)

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
        elif len(rows) == 0:
            return True
        else:
            return False

    def generate_new_asset_id(self, order: Order) -> int:
        """
        Generates a new unique ID for use within the table. \n
        :param order: the order, used to generate a prefix based on trade type.
        :return: id.
        """
        pref: str = "1" if order.type == OrderType.BUY else "2"
        new_id: int = int(pref + str(random.randrange(100000)))
        if self.is_order_id_unique(new_id):
            return new_id
        else:
            return self.generate_new_asset_id(order)
