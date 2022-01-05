import alpaca_trade_api as tradeapi
from config import ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, ALPACA_PAPER_ADDRESS, ALPACA_PAPER_ACCOUNT_NUMBER


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
