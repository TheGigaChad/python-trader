import alpaca_trade_api as tradeapi
import pytest

from pytrader.config import ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, ALPACA_PAPER_ADDRESS, ALPACA_PAPER_ACCOUNT_NUMBER
from pytrader.exchange.exchangeManager import ExchangeManager


# ALPACA TESTS
def test_alpaca_paper_account():
    api = tradeapi.REST(ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, ALPACA_PAPER_ADDRESS)
    assert api.get_account().account_number == ALPACA_PAPER_ACCOUNT_NUMBER


def test_alpaca_paper_account_blocked():
    api = tradeapi.REST(ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, ALPACA_PAPER_ADDRESS)
    assert not api.get_account().account_blocked


def test_alpaca_paper_trading_blocked():
    api = tradeapi.REST(ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, ALPACA_PAPER_ADDRESS)
    assert not api.get_account().trading_blocked


def test_alpaca_paper_transfers_blocked():
    api = tradeapi.REST(ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, ALPACA_PAPER_ADDRESS)
    assert not api.get_account().transfers_blocked


def test_exchange_paper_stock_account():
    exchange = ExchangeManager(is_testing=True)
    cash = exchange.paper_stock_exchange.cash
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
