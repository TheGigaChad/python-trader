import alpaca_trade_api as trade_api
import pytest
from alpaca_trade_api.common import URL

from pytrader import config, exchange, common

# ALPACA TESTS
ALPACA_API = trade_api.REST(config.ALPACA_PAPER_KEY, config.ALPACA_PAPER_SECRET, URL(config.ALPACA_PAPER_ADDRESS))
RUN_TYPE: common.RunType = common.RunType.TEST


def test_alpaca_paper_account():
    assert ALPACA_API.get_account().account_number == config.ALPACA_PAPER_ACCOUNT_NUMBER


def test_alpaca_paper_account_blocked():
    assert not ALPACA_API.get_account().account_blocked


def test_alpaca_paper_trading_blocked():
    assert not ALPACA_API.get_account().trading_blocked


def test_alpaca_paper_transfers_blocked():
    assert not ALPACA_API.get_account().transfers_blocked


def test_exchange_paper_stock_account():
    e: exchange.ExchangeManager = exchange.ExchangeManager(run_type=RUN_TYPE)
    cash = e.paper_stock_exchange.cash
    assert cash is not None and type(cash) == float


@pytest.mark.xfail
def test_exchange_paper_stock_buy():
    # # create an order
    # asset_name: str = "TSLA"
    # asset_type: common.AssetType = common.AssetType.PAPER_STOCK
    # order: common.Order = common.Order(common.OrderType.BUY, common.Asset(asset_name, asset_type))
    # order.status = common.OrderStatus.QUEUED
    #
    # # fulfill order
    # e: exchange.ExchangeManager = exchange.ExchangeManager(run_type=RUN_TYPE)
    # status: common.GenericStatus = e.fulfill_order(order)
    #
    # assert status == common.GenericStatus.SUCCESSFUL
    pass

@pytest.mark.xfail
def test_exchange_paper_stock_sell():
    # TODO - we should modify managers to be able to run exclusively one trade to make this simple.
    pass


@pytest.mark.xfail
def test_exchange_paper_crypto_account():
    pass


@pytest.mark.xfail
def test_exchange_stock_account():
    pass


@pytest.mark.xfail
def test_exchange_crypto_account():
    pass
