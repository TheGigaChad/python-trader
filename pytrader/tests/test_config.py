from pytrader import config


def test_trade_ratios():
    assert (config.USER_RISK_PARITY_RATIO + config.USER_SHORT_TERM_TRADE_RATIO + config.USER_LONG_TERM_TRADE_RATIO) == 1

