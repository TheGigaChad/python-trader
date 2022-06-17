from datetime import datetime
from typing import Tuple, List

from pytrader import common, config
from pytrader.sql import sqlDb

Log: common.Log = common.Log(__file__)


class SQLDbBuySellThresholds(sqlDb.SQLDb):

    def __init__(self):
        super().__init__(sqlDb.SQLDbType.BUY_SELL_THRESHOLDS)
        self.__column_name: str = config.SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_NAME
        self.__column_buy: str = config.SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_BUY
        self.__column_sell: str = config.SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_SELL
        self.__column_last_updated: str = config.SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_LAST_UPDATED

    def get_threshold(self, asset: common.Asset) -> Tuple[float, float]:
        """
        Gets the thresholds for the specific asset, returns default values if it doesn't exist.  To be fair this should
        be a massive red flag and require some recalculations...
        :param asset: The asset we are trying to inspect for.
        :return: buy and sell thresholds, defaults to default values if cannot find them.
        """
        # TODO - what if it doesnt exist?  Should we queue it??
        rows, headers = self.run_sql_query(f"SELECT buy, sell FROM {self.table_name} WHERE name = '{asset.name}';")
        if len(rows) == 1:
            return rows[0][0], rows[0][1]
        else:
            Log.d(f"tradingManager.determineBuySellThresholdValues - no db entry for {asset.name}. creating now...")
            query = f"INSERT INTO {self.table_name} (`name`, `buy`, `sell`, `last_updated`) VALUES (%s, '1.0','-1.0',%s);"
            params = [asset.name, datetime.now().__str__()]
            success: sqlDb.SQLQueryResponseType = self.run_sql_query_no_response(query, params)
            if success:
                rows, headers = self.run_sql_query(
                    f"SELECT buy, sell FROM {self.table_name} WHERE name = '{asset.name}';")
                return rows[0][0], rows[0][1]
            Log.w(f"determineBuySellThresholdValues - couldn't create new entry for {asset.name}.")

    def get_thresholds(self) -> List:
        """
        Gets the thresholds for all assets from db.
        :return: buy and sell thresholds, defaults to default values if cannot find them.
        """
        # TODO - what if it doesnt exist?  Should we queue it??
        rows, headers = self.run_sql_query(f"SELECT name, buy, sell, last_updated "
                                           f"FROM {self.table_name} WHERE name LIKE '%';")
        return rows if rows is not None else []
