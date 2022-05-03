import datetime
import json

import mysql.connector as mysql

from pytrader.SQL.sqlDb.sqlDb import SQLQueryResponseType
from pytrader.common.requests import RequestType, ResponseType
from pytrader.exchange.exchange import ExchangeName
from pytrader.trade.tradingManager import determineBuySellThresholdValues
from pytrader.marketData.marketData_SQL import getSQLWindowDataAsJson, updateWindowData
from pytrader.SQL.sqlDb.sqlDbTrades import SQLDbTrades, SQLDbTradesDao

from pytrader.config import SQL_SERVER_HOST, SQL_SERVER_DATABASE, SQL_SERVER_USER, SQL_SERVER_PASSWORD, \
    SQL_SERVER_WINDOWS_TABLE, SQL_SERVER_BUY_SELL_THRESHOLDS_TABLE


def test_connection():
    db_connection = mysql.connect(host=SQL_SERVER_HOST, database=SQL_SERVER_DATABASE, user=SQL_SERVER_USER,
                                  password=SQL_SERVER_PASSWORD)
    assert db_connection.is_connected()


def test_sql_get_algo_windows():
    db_connection = mysql.connect(host=SQL_SERVER_HOST, database=SQL_SERVER_DATABASE, user=SQL_SERVER_USER,
                                  password=SQL_SERVER_PASSWORD)
    cursor = db_connection.cursor()
    sql_command = f"SELECT * FROM {SQL_SERVER_WINDOWS_TABLE} WHERE 1"
    cursor.execute(sql_command)
    response = cursor.fetchall()
    cursor.close()
    assert len(response) > 0


def is_json(item) -> bool:
    try:
        json_object = json.dumps(item)
    except ValueError as e:
        return False
    return True


def test_sql_window_data_to_json():
    json_data = getSQLWindowDataAsJson()
    assert is_json(json_data)


def test_sql_save_window_data():
    json_file = "test_algo_windows.json"

    # empty the data
    open(json_file, 'w').close()

    # make sure data is gone
    with open(json_file, "r") as infile:
        assert infile.readable()
        assert len(infile.readlines()) == 0
        infile.close()

    updateWindowData(file_name=json_file)

    # make sure data is written
    with open(json_file, "r") as infile:
        assert infile.readable()
        assert len(infile.readlines()) > 0
        infile.close()


def test_sql_get_buy_sell_thresholds():
    db_connection = mysql.connect(host=SQL_SERVER_HOST, database=SQL_SERVER_DATABASE, user=SQL_SERVER_USER,
                                  password=SQL_SERVER_PASSWORD)
    cursor = db_connection.cursor()
    sql_command = f"SELECT * FROM {SQL_SERVER_BUY_SELL_THRESHOLDS_TABLE} WHERE 1"
    cursor.execute(sql_command)
    response = cursor.fetchall()
    cursor.close()
    assert len(response) > 0


def test_sql_get_buy_sell_threshold_values():
    asset_name = "TSLA"
    buy, sell = determineBuySellThresholdValues(asset_name)
    assert buy is not None
    assert sell is not None


def test_sql_get_buy_sell_threshold_values_creation():
    asset_name = "TSLAA"
    buy, sell = determineBuySellThresholdValues(asset_name)
    print(buy, sell)


# ========== TRADES ===============
def test_sql_trades_get_trade():
    asset_name: str = "TEST"
    order_type: str = "BUY"
    quantity: float = 1
    order_id: int = 1
    timestamp_str: str = "2022-04-28 03:44:03"
    exchange: str = "ALPACA_PAPER"

    sql_db: SQLDbTrades = SQLDbTrades()
    trade_dao: SQLDbTradesDao = sql_db.getTradeByOrderId(order_id)

    assert trade_dao.name == asset_name
    assert trade_dao.order_type == order_type
    assert trade_dao.quantity == quantity
    assert trade_dao.order_id == order_id
    assert str(trade_dao.timestamp) == timestamp_str
    assert trade_dao.exchange == exchange


def test_sql_trades_get_all_buy_trades():
    sql_db: SQLDbTrades = SQLDbTrades()
    trades_dao: [SQLDbTradesDao] = sql_db.getAllBuyTrades()
    assert len(trades_dao) == 1


def test_sql_trades_get_all_sell_trades():
    sql_db: SQLDbTrades = SQLDbTrades()
    trades_dao: [SQLDbTradesDao] = sql_db.getAllSellTrades()
    assert len(trades_dao) == 1


def test_sql_trades_commit_trade():
    asset_name: str = "TEST"
    order_type: RequestType = RequestType.BUY
    quantity: float = 1.23
    order_id: int = 0
    timestamp: datetime.datetime = datetime.datetime.now()
    exchange: ExchangeName = ExchangeName.ALPACA_PAPER

    # commit trade to db
    sql_db: SQLDbTrades = SQLDbTrades()
    dao: SQLDbTradesDao = SQLDbTradesDao(asset_name, order_type, quantity, order_id, timestamp, exchange)
    response: SQLQueryResponseType = sql_db.commitTrade(dao)
    assert response == SQLQueryResponseType.SUCCESSFUL

    # get created trade from db
    get_dao: SQLDbTradesDao = sql_db.getTradeByOrderId(order_id)
    assert get_dao is not None

    # delete created trade from db
    delete_successful = sql_db.deleteTrade(dao)
    assert delete_successful == SQLQueryResponseType.SUCCESSFUL

    # make sure its gone
    get_dao = sql_db.getTradeByOrderId(order_id)
    assert get_dao is None
