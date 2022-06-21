from typing import List, Optional

from pytrader import common
from pytrader import config
from pytrader.sql import sqlDb


class SQLDbWindows(sqlDb.SQLDb):
    def __init__(self):
        super().__init__(sqlDb.SQLDbType.WINDOW)
        self.__column_name: str = config.SQL_SERVER_WINDOWS_COLUMN_NAME
        self.__column_sma_short_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_SMA_SHORT_TRADE
        self.__column_sma_long_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_SMA_LONG_TRADE
        self.__column_sma_long_hold: str = config.SQL_SERVER_WINDOWS_COLUMN_SMA_LONG_HOLD
        self.__column_ema_short_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_EMA_SHORT_TRADE
        self.__column_ema_long_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_EMA_LONG_TRADE
        self.__column_ema_long_hold: str = config.SQL_SERVER_WINDOWS_COLUMN_EMA_LONG_HOLD
        self.__column_macd_fast_short_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_SHORT_TRADE
        self.__column_macd_slow_short_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_SHORT_TRADE
        self.__column_macd_sig_short_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_SHORT_TRADE
        self.__column_macd_fast_long_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_LONG_TRADE
        self.__column_macd_slow_long_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_LONG_TRADE
        self.__column_macd_sig_long_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_LONG_TRADE
        self.__column_macd_fast_long_hold: str = config.SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_LONG_HOLD
        self.__column_macd_slow_long_hold: str = config.SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_LONG_HOLD
        self.__column_macd_sig_long_hold: str = config.SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_LONG_HOLD
        self.__column_rsi_short_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_RSI_SHORT_TRADE
        self.__column_rsi_long_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_RSI_LONG_TRADE
        self.__column_rsi_long_hold: str = config.SQL_SERVER_WINDOWS_COLUMN_RSI_LONG_HOLD
        self.__column_vol_short_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_VOL_SHORT_TRADE
        self.__column_vol_long_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_VOL_LONG_TRADE
        self.__column_vol_long_hold: str = config.SQL_SERVER_WINDOWS_COLUMN_VOL_LONG_HOLD
        self.__column_bolb_short_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_BOLB_SHORT_TRADE
        self.__column_bolb_long_trade: str = config.SQL_SERVER_WINDOWS_COLUMN_BOLB_LONG_TRADE
        self.__column_bolb_long_hold: str = config.SQL_SERVER_WINDOWS_COLUMN_BOLB_LONG_HOLD

    @staticmethod
    def __create_dao(row: List) -> sqlDb.daos.SQLDbWindowsDao:
        """
        creates a DAO object from the sql row.
        :param row: sql row object
        :return: dao object containing all the row data.
        """
        return sqlDb.daos.SQLDbWindowsDao(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                                          row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16],
                                          row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24])

    def get_window(self, asset: common.Asset) -> Optional[sqlDb.daos.SQLDbWindowsDao]:
        """
        retrieves the window data for specified asset.  This will contain all params used for inspecting whether a
        trade is worthwhile. \n
        :param asset: specified asset that we want data for.
        :return: dao object with all relevant data, or None if doesn't exist.
        """
        query = f"SELECT * FROM `{super().table_name}` WHERE {self.__column_name} = {asset.name}"
        rows, columns = self.run_sql_query(query)
        if len(rows) == 0:
            return None
        return self.__create_dao(rows[0])

    def get_windows(self) -> List:
        """
        retrieves all window data for all saved assets.
        :return: list of all data as ROWS.
        """
        query = f"SELECT * FROM `{super().table_name}` WHERE {self.__column_name} LIKE '%';"
        rows, columns = self.run_sql_query(query)
        if len(rows) == 0:
            return []
        windows: List = []
        for row in rows:
            windows.append(self.__create_dao(row))
        return windows
