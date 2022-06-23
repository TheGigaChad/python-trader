import datetime
import json
from pathlib import Path
from typing import List

import mysql.connector as mysql

from pytrader import cfg as cfg
from pytrader import common
from pytrader.marketData.marketData_SQL import get_sql_window_data_as_json, update_window_data
from pytrader.sql import sqlDb as sqlDb

THIS_DIR = Path(__file__).parent
DATA_PATH = THIS_DIR / 'data'


@common.timed
def test_sql_connection():
    """
    Tests the connection to the sql server.
    """
    db_connection = mysql.connect(host=cfg.SQL_SERVER_HOST, database=cfg.SQL_SERVER_DATABASE, user=cfg.SQL_SERVER_USER,
                                  password=cfg.SQL_SERVER_PASSWORD)
    assert db_connection.is_connected()


@common.timed
def test_sql_table_windows_data():
    """
    Tests the connection to the windows table and checks whether at least one thing exists
    """
    db: sqlDb.sqlDbWindows = sqlDb.SQLDbWindows()
    windows: List = db.get_windows()
    assert len(windows) > 0


@common.timed
def test_sql_table_buy_sell_threshold_data():
    """
    Tests the connection to the buy sell threshold table and checks whether at least one thing exists
    """
    db: sqlDb.SQLDbBuySellThresholds = sqlDb.SQLDbBuySellThresholds()
    thresholds: List = db.get_thresholds()
    assert len(thresholds) > 0


@common.timed
def test_sql_table_trades_data():
    """
    Tests the connection to the trade table and checks whether at least one thing exists
    """
    # TODO - redo to use method
    db: sqlDb.SQLDbTrades = sqlDb.SQLDbTrades()
    trades: List = db.get_all_trades()
    assert len(trades) > 0


def is_json(item) -> bool:
    try:
        json_object = json.dumps(item)
    except ValueError as e:
        return False
    return True


@common.timed
def test_sql_window_data_to_json():
    # TODO - do we need this? not sure anymore...
    json_data = get_sql_window_data_as_json()
    assert is_json(json_data)


@common.timed
def test_sql_save_window_data():
    json_file: str = str(DATA_PATH / "test_algo_windows.json")

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


@common.timed
def test_sql_get_buy_sell_threshold_values():
    """
    Tests that we can retrieve the buy and sell threshold values from the database.
    """
    asset_name = "TSLA"
    asset_type: common.AssetType = common.AssetType.PAPER_STOCK
    asset: common.Asset = common.Asset(asset_name, asset_type)

    db: sqlDb.SQLDbBuySellThresholds = sqlDb.SQLDbBuySellThresholds()
    buy_threshold, sell_threshold = db.get_threshold(asset)
    assert buy_threshold is not None
    assert sell_threshold is not None


# ========== TRADES ===============
@common.timed
def test_sql_trades_get_trade():
    """
    Tests that we can retrieve a trade from the trade database.
    """
    asset_name: str = "TEST"
    order_type: common.OrderType = common.OrderType.BUY
    quantity: float = 1
    order_id: int = 1
    timestamp_str: str = "2022-04-28 03:44:03"
    asset_type: common.AssetType = common.AssetType.PAPER_STOCK

    sql_db: sqlDb.SQLDbTrades = sqlDb.SQLDbTrades()
    trade_dao: sqlDb.daos.SQLDbTradesDao = sql_db.get_trade_by_order_id(order_id)

    assert trade_dao.name == asset_name
    assert trade_dao.order_type == order_type.value
    assert trade_dao.quantity == quantity
    assert trade_dao.order_id == order_id
    assert str(trade_dao.timestamp) == timestamp_str
    assert trade_dao.asset_type == asset_type.value


@common.timed
def test_sql_trades_get_all_buy_trades():
    """
    Tests that we can retrieve all buy trades from the database.
    """
    sql_db: sqlDb.SQLDbTrades = sqlDb.SQLDbTrades()
    trades_dao: [sqlDb.daos.SQLDbTradesDao] = sql_db.get_all_buy_trades()
    assert len(trades_dao) == 1


@common.timed
def test_sql_trades_get_all_sell_trades():
    """
    Tests that we can retrieve all sell trades from the database.
    """
    sql_db: sqlDb.SQLDbTrades = sqlDb.SQLDbTrades()
    trades_dao: [sqlDb.daos.SQLDbTradesDao] = sql_db.get_all_sell_trades()
    assert len(trades_dao) == 1


@common.timed
def test_sql_trades_commit_trade():
    """
    Tests that we are able to add a trade to the sql database.  We then delete it for cleanliness purposes.
    """
    asset_name: str = "TEST"
    order_type: common.OrderType = common.OrderType.BUY
    quantity: float = 1.23
    order_id: int = 0
    timestamp: datetime.datetime = datetime.datetime.now()
    asset_type: common.AssetType = common.AssetType.PAPER_STOCK
    trade_intent: common.TradeIntent = common.TradeIntent.SHORT_TRADE

    # commit trade to db
    sql_db: sqlDb.SQLDbTrades = sqlDb.SQLDbTrades()
    order: common.Order = common.Order(order_type, common.Asset(asset_name, asset_type))
    order.asset.qty = quantity
    order.asset.id = order_id
    order.asset.trade_intent = trade_intent
    response: sqlDb.SQLQueryResponseType = sql_db.commit_trade(order)
    assert response == sqlDb.SQLQueryResponseType.SUCCESSFUL

    # get created trade from db
    get_dao: sqlDb.daos.SQLDbTradesDao = sql_db.get_trade_by_order_id(order_id)
    assert get_dao is not None

    # delete created trade from db
    delete_successful = sql_db.delete_trade(order)
    assert delete_successful == sqlDb.SQLQueryResponseType.SUCCESSFUL

    # make sure its gone
    get_dao = sql_db.get_trade_by_order_id(order_id)
    assert get_dao is None


@common.timed
def test_sql_open_trades_commit_trade():
    """
    Tests that we are able to add a trade to the sql database.  We then delete it for cleanliness purposes.
    """
    asset_name: str = "TEST"
    order_id: int = 0
    # commit trade to db
    sql_db: sqlDb.SQLDbOpenTrades = sqlDb.SQLDbOpenTrades()
    order: common.Order = common.Order(common.OrderType.BUY, common.Asset(asset_name, common.AssetType.PAPER_STOCK))
    order.asset.qty = 1.23
    order.asset.id = order_id
    order.asset.trade_intent = common.TradeIntent.SHORT_TRADE
    response: sqlDb.SQLQueryResponseType = sql_db.commit_trade(order)
    assert response == sqlDb.SQLQueryResponseType.SUCCESSFUL

    # get created trade from db
    get_dao: sqlDb.daos.SQLDbOpenTradesDao = sql_db.get_trade_by_order_id(order_id)
    assert get_dao is not None

    # delete created trade from db
    delete_successful = sql_db.delete_trade(order)
    assert delete_successful == sqlDb.SQLQueryResponseType.SUCCESSFUL

    # make sure its gone
    get_dao = sql_db.get_trade_by_order_id(order_id)
    assert get_dao is None


@common.timed
def test_sql_open_trades_unique_id():
    asset_name: str = "TEST"
    order_id: int = 0
    # commit trade to db
    sql_db: sqlDb.SQLDbOpenTrades = sqlDb.SQLDbOpenTrades()
    order: common.Order = common.Order(common.OrderType.BUY, common.Asset(asset_name, common.AssetType.PAPER_STOCK))
    order.asset.qty = 1.23
    order.asset.id = order_id
    order.asset.trade_intent = common.TradeIntent.SHORT_TRADE
    response: bool = sql_db.is_order_id_unique(order.asset.id)
    assert response


@common.timed
def test_sql_open_trades_generate_unique_id():
    asset_name: str = "TEST"
    order_id: int = 0
    # commit trade to db
    sql_db: sqlDb.SQLDbOpenTrades = sqlDb.SQLDbOpenTrades()
    order: common.Order = common.Order(common.OrderType.BUY, common.Asset(asset_name, common.AssetType.PAPER_STOCK))
    order.asset.qty = 1.23
    order.asset.id = order_id
    order.asset.trade_intent = common.TradeIntent.SHORT_TRADE
    new_id: int = sql_db.generate_new_asset_id(order)
    assert new_id != 0


@common.timed
def test_sql_open_trades_update_order():
    asset_name: str = "TEST"
    order_id: int = 0
    # commit trade to db
    sql_db: sqlDb.SQLDbOpenTrades = sqlDb.SQLDbOpenTrades()
    order: common.Order = common.Order(common.OrderType.BUY, common.Asset(asset_name, common.AssetType.PAPER_STOCK))
    order.asset.qty = 1.23
    order.asset.id = order_id
    order.asset.trade_intent = common.TradeIntent.SHORT_TRADE
    response: sqlDb.SQLQueryResponseType = sql_db.commit_trade(order)
    assert response == sqlDb.SQLQueryResponseType.SUCCESSFUL

    order.asset.last_updated = datetime.datetime.min
    response = sql_db.update_trade(order)
    assert response == sqlDb.SQLQueryResponseType.SUCCESSFUL

    new_order: sqlDb.daos.SQLDbOpenTradesDao = sql_db.get_trade_by_order_id(order.asset.id)
    assert new_order.timestamp == datetime.datetime.min

    # delete created trade from db
    delete_successful = sql_db.delete_trade(order)
    assert delete_successful == sqlDb.SQLQueryResponseType.SUCCESSFUL

    # make sure its gone
    get_dao = sql_db.get_trade_by_order_id(order_id)
    assert get_dao is None
