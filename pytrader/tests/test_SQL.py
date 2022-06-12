import datetime
import json

import mysql.connector as mysql

from pytrader import cfg as cfg
from pytrader.SQL.sqlDb.Daos.sqlDbOpenTradesDao import SQLDbOpenTradesDao
from pytrader.SQL.sqlDb.sqlDb import SQLQueryResponseType
from pytrader.SQL.sqlDb.sqlDbOpenTrades import SQLDbOpenTrades
from pytrader.SQL.sqlDb.sqlDbTrades import SQLDbTrades, SQLDbTradesDao
from pytrader.algo.algo_tradeIntent import TradeIntent
from pytrader.common.asset import Asset, AssetType
from pytrader.common.order import OrderType, Order
from pytrader.common.requests import RequestType
from pytrader.common.wrappers import timed
from pytrader.exchange.exchange import ExchangeName
from pytrader.marketData.marketData_SQL import get_sql_window_data_as_json, update_window_data
from pytrader.trade.tradingManager import determine_buy_sell_threshold_values


@timed
def test_sql_connection():
    """
    Tests the connection to the SQL server.
    """
    db_connection = mysql.connect(host=cfg.SQL_SERVER_HOST, database=cfg.SQL_SERVER_DATABASE, user=cfg.SQL_SERVER_USER,
                                  password=cfg.SQL_SERVER_PASSWORD)
    assert db_connection.is_connected()


@timed
def test_sql_table_windows_data():
    """
    Tests the connection to the windows table and checks whether at least one thing exists
    """
    # TODO - redo to use method
    db_connection = mysql.connect(host=cfg.SQL_SERVER_HOST, database=cfg.SQL_SERVER_DATABASE, user=cfg.SQL_SERVER_USER,
                                  password=cfg.SQL_SERVER_PASSWORD)
    cursor = db_connection.cursor()
    sql_command = f"SELECT * FROM {cfg.SQL_SERVER_WINDOWS_TABLE} WHERE 1"
    cursor.execute(sql_command)
    response = cursor.fetchall()
    cursor.close()
    assert len(response) > 0


@timed
def test_sql_table_buy_sell_threshold_data():
    """
    Tests the connection to the buy sell threshold table and checks whether at least one thing exists
    """
    # TODO - redo to use method
    db_connection = mysql.connect(host=cfg.SQL_SERVER_HOST, database=cfg.SQL_SERVER_DATABASE, user=cfg.SQL_SERVER_USER,
                                  password=cfg.SQL_SERVER_PASSWORD)
    cursor = db_connection.cursor()
    sql_command = f"SELECT * FROM {cfg.SQL_SERVER_BUY_SELL_THRESHOLDS_TABLE} WHERE 1"
    cursor.execute(sql_command)
    response = cursor.fetchall()
    cursor.close()
    assert len(response) > 0


@timed
def test_sql_table_trades_data():
    """
    Tests the connection to the trade table and checks whether at least one thing exists
    """
    # TODO - redo to use method
    db_connection = mysql.connect(host=cfg.SQL_SERVER_HOST, database=cfg.SQL_SERVER_DATABASE, user=cfg.SQL_SERVER_USER,
                                  password=cfg.SQL_SERVER_PASSWORD)
    cursor = db_connection.cursor()
    sql_command = f"SELECT * FROM {cfg.SQL_SERVER_TRADES_TABLE} WHERE 1"
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


@timed
def test_sql_window_data_to_json():
    json_data = get_sql_window_data_as_json()
    assert is_json(json_data)


@timed
def test_sql_save_window_data():
    json_file = "test_algo_windows.json"

    # empty the data
    open(json_file, 'w').close()

    # make sure data is gone
    with open(json_file, "r") as infile:
        assert infile.readable()
        assert len(infile.readlines()) == 0
        infile.close()

    update_window_data(file_name=json_file)

    # make sure data is written
    with open(json_file, "r") as infile:
        assert infile.readable()
        assert len(infile.readlines()) > 0
        infile.close()


@timed
def test_sql_get_buy_sell_threshold_values():
    """
    Tests that we can retrieve the buy and sell threshold values from the database.
    """
    asset_name = "TSLA"
    buy, sell = determine_buy_sell_threshold_values(asset_name)
    assert buy is not None
    assert sell is not None


@timed
def test_sql_get_buy_sell_threshold_values_creation():
    """
    Tests that we can create the buy and sell threshold values from the database if they do not exist. We then
    delete afterwards.
    """
    asset_name = "TSLAA"
    buy, sell = determine_buy_sell_threshold_values(asset_name)
    assert buy == 1.0
    assert sell == -1.0


# ========== TRADES ===============
@timed
def test_sql_trades_get_trade():
    """
    Tests that we can retrieve a trade from the trade database.
    """
    asset_name: str = "TEST"
    order_type: OrderType = OrderType.BUY
    quantity: float = 1
    order_id: int = 1
    timestamp_str: str = "2022-04-28 03:44:03"
    exchange: ExchangeName = ExchangeName.ALPACA_PAPER

    sql_db: SQLDbTrades = SQLDbTrades()
    trade_dao: SQLDbTradesDao = sql_db.get_trade_by_order_id(order_id)

    assert trade_dao.name == asset_name
    assert trade_dao.order_type == order_type.value
    assert trade_dao.quantity == quantity
    assert trade_dao.order_id == order_id
    assert str(trade_dao.timestamp) == timestamp_str
    assert trade_dao.exchange == exchange.value


@timed
def test_sql_trades_get_all_buy_trades():
    """
    Tests that we can retrieve all buy trades from the database.
    """
    sql_db: SQLDbTrades = SQLDbTrades()
    trades_dao: [SQLDbTradesDao] = sql_db.get_all_buy_trades()
    assert len(trades_dao) == 1


@timed
def test_sql_trades_get_all_sell_trades():
    """
    Tests that we can retrieve all sell trades from the database.
    """
    sql_db: SQLDbTrades = SQLDbTrades()
    trades_dao: [SQLDbTradesDao] = sql_db.get_all_sell_trades()
    assert len(trades_dao) == 1


@timed
def test_sql_trades_commit_trade():
    """
    Tests that we are able to add a trade to the sql database.  We then delete it for cleanliness purposes.
    """
    asset_name: str = "TEST"
    order_type: RequestType = RequestType.BUY
    quantity: float = 1.23
    order_id: int = 0
    timestamp: datetime.datetime = datetime.datetime.now()
    exchange: ExchangeName = ExchangeName.ALPACA_PAPER

    # commit trade to db
    sql_db: SQLDbTrades = SQLDbTrades()
    dao: SQLDbTradesDao = SQLDbTradesDao(asset_name, order_type, quantity, order_id, timestamp, exchange)
    response: SQLQueryResponseType = sql_db.commit_trade(dao)
    assert response == SQLQueryResponseType.SUCCESSFUL

    # get created trade from db
    get_dao: SQLDbTradesDao = sql_db.get_trade_by_order_id(order_id)
    assert get_dao is not None

    # delete created trade from db
    delete_successful = sql_db.delete_trade(dao)
    assert delete_successful == SQLQueryResponseType.SUCCESSFUL

    # make sure its gone
    get_dao = sql_db.get_trade_by_order_id(order_id)
    assert get_dao is None


@timed
def test_sql_open_trades_commit_trade():
    """
    Tests that we are able to add a trade to the sql database.  We then delete it for cleanliness purposes.
    """
    asset_name: str = "TEST"
    order_id: int = 0
    # commit trade to db
    sql_db: SQLDbOpenTrades = SQLDbOpenTrades()
    order: Order = Order(OrderType.BUY, Asset(asset_name, AssetType.PAPER_STOCK))
    order.asset.qty = 1.23
    order.asset.id = order_id
    order.asset.trade_intent = TradeIntent.SHORT_TRADE
    response: SQLQueryResponseType = sql_db.commit_trade(order)
    assert response == SQLQueryResponseType.SUCCESSFUL

    # get created trade from db
    get_dao: SQLDbOpenTradesDao = sql_db.get_trade_by_order_id(order_id)
    assert get_dao is not None

    # delete created trade from db
    delete_successful = sql_db.delete_trade(order)
    assert delete_successful == SQLQueryResponseType.SUCCESSFUL

    # make sure its gone
    get_dao = sql_db.get_trade_by_order_id(order_id)
    assert get_dao is None


@timed
def test_sql_open_trades_unique_id():
    asset_name: str = "TEST"
    order_id: int = 0
    # commit trade to db
    sql_db: SQLDbOpenTrades = SQLDbOpenTrades()
    order: Order = Order(OrderType.BUY, Asset(asset_name, AssetType.PAPER_STOCK))
    order.asset.qty = 1.23
    order.asset.id = order_id
    order.asset.trade_intent = TradeIntent.SHORT_TRADE
    response: bool = sql_db.is_order_id_unique(order.asset.id)
    assert response


@timed
def test_sql_open_trades_generate_unique_id():
    asset_name: str = "TEST"
    order_id: int = 0
    # commit trade to db
    sql_db: SQLDbOpenTrades = SQLDbOpenTrades()
    order: Order = Order(OrderType.BUY, Asset(asset_name, AssetType.PAPER_STOCK))
    order.asset.qty = 1.23
    order.asset.id = order_id
    order.asset.trade_intent = TradeIntent.SHORT_TRADE
    new_id: int = sql_db.generate_new_asset_id(order)
    assert new_id != 0

@timed
def test_sql_open_trades_update_order():
    asset_name: str = "TEST"
    order_id: int = 0
    # commit trade to db
    sql_db: SQLDbOpenTrades = SQLDbOpenTrades()
    order: Order = Order(OrderType.BUY, Asset(asset_name, AssetType.PAPER_STOCK))
    order.asset.qty = 1.23
    order.asset.id = order_id
    order.asset.trade_intent = TradeIntent.SHORT_TRADE
    response: SQLQueryResponseType = sql_db.commit_trade(order)
    assert response == SQLQueryResponseType.SUCCESSFUL

    order.asset.last_updated = datetime.datetime.min
    response = sql_db.update_trade(order)
    assert response == SQLQueryResponseType.SUCCESSFUL

    new_order: SQLDbOpenTradesDao = sql_db.get_trade_by_order_id(order.asset.id)
    assert new_order.timestamp == datetime.datetime.min

    # delete created trade from db
    delete_successful = sql_db.delete_trade(order)
    assert delete_successful == SQLQueryResponseType.SUCCESSFUL

    # make sure its gone
    get_dao = sql_db.get_trade_by_order_id(order_id)
    assert get_dao is None
