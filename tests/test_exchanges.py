import pytest
import alpaca_trade_api as tradeapi
from algo_config import ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET


# ALPACA TESTS
#@pytest.mark.xfail
def test_alpaca_paper_account():
    api = tradeapi.REST(ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, 'https://paper-api.alpaca.markets')
    account_number = "PA3Y2VIN22VU"
    assert api.get_account().account_number == account_number


#@pytest.mark.xfail
def test_alpaca_paper_account_blocked():
    api = tradeapi.REST(ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, 'https://paper-api.alpaca.markets')
    assert not api.get_account().account_blocked


#@pytest.mark.xfail
def test_alpaca_paper_trading_blocked():
    api = tradeapi.REST(ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, 'https://paper-api.alpaca.markets')
    assert not api.get_account().trading_blocked


#@pytest.mark.xfail
def test_alpaca_paper_transfers_blocked():
    api = tradeapi.REST(ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET, 'https://paper-api.alpaca.markets')
    assert not api.get_account().transfers_blocked
