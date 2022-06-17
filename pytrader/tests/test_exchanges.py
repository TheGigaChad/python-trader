import alpaca_trade_api as trade_api
import pytest

from pytrader import config, exchange


# ALPACA TESTS
def test_alpaca_paper_account():
    api = trade_api.REST(config.ALPACA_PAPER_KEY, config.ALPACA_PAPER_SECRET, config.ALPACA_PAPER_ADDRESS)
    assert api.get_account().account_number == config.ALPACA_PAPER_ACCOUNT_NUMBER


def test_alpaca_paper_account_blocked():
    api = trade_api.REST(config.ALPACA_PAPER_KEY, config.ALPACA_PAPER_SECRET, config.ALPACA_PAPER_ADDRESS)
    assert not api.get_account().account_blocked


def test_alpaca_paper_trading_blocked():
    api = trade_api.REST(config.ALPACA_PAPER_KEY, config.ALPACA_PAPER_SECRET, config.ALPACA_PAPER_ADDRESS)
    assert not api.get_account().trading_blocked


def test_alpaca_paper_transfers_blocked():
    api = trade_api.REST(config.ALPACA_PAPER_KEY, config.ALPACA_PAPER_SECRET, config.ALPACA_PAPER_ADDRESS)
    assert not api.get_account().transfers_blocked


def test_exchange_paper_stock_account():
    e: exchange.ExchangeManager = exchange.ExchangeManager(is_testing=True)
    cash = e.paper_stock_exchange.cash
    assert cash is not None and type(cash) == float


@pytest.mark.xfail
def test_exchange_paper_stock_buy():
    pass
    # exchange = ExchangeManager(is_testing=True)
    # asset = Asset("TSLA", AssetType.PAPER_STOCK)
    # exchange.request(asset=asset, request_type=RequestType.BUY)


@pytest.mark.xfail
def test_exchange_paper_stock_sell():
    pass
    # exchange = ExchangeManager(isTesting=True)
    # asset = Asset("TSLA", AssetType.PAPER_STOCK)
    # exchange.request(asset=asset, request_type=RequestType.SELL)


@pytest.mark.xfail
def test_exchange_paper_crypto_account():
    pass


@pytest.mark.xfail
def test_exchange_stock_account():
    pass


@pytest.mark.xfail
def test_exchange_crypto_account():
    pass
