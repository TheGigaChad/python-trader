from pathlib import Path

import pandas as pd
import pytest

from pytrader import common
from pytrader import marketData

DIR_PATH: Path = Path(__file__).parent
DATA_DIR_PATH: Path = DIR_PATH / 'data'
STOCK_DATA = pd.read_csv(DATA_DIR_PATH / "TSLA_historical_data.csv")
STOCK_NAME: str = "TSLA"
WINDOWS_TEST_JSON_PATH: Path = DIR_PATH / "data/test_algo_windows.json"


def test_rsi():
    """
    Tests the relative strength Index method against a pre-calculated value.
    """
    trade_intent = common.TradeIntent.SHORT_TRADE
    indicator = common.Indicator.RSI
    window = marketData.get_window(indicator, trade_intent, STOCK_NAME, str(WINDOWS_TEST_JSON_PATH))
    rsi_data = marketData.get_RSI(window, STOCK_DATA).dropna()
    first_point = rsi_data.iloc[0]
    last_point = rsi_data.iloc[-1]
    assert first_point == 69.87030283020084 and last_point == 56.124583112389


def test_bollinger():
    """
    Tests the Relative Strength Index method against a pre-calculated value.
    """
    trade_intent = common.TradeIntent.SHORT_TRADE
    indicator = common.Indicator.BOLLINGER
    window = marketData.get_window(indicator, trade_intent, STOCK_NAME, str(WINDOWS_TEST_JSON_PATH))
    bollinger_data = marketData.append_bollinger(window, STOCK_DATA).dropna()
    first_point = bollinger_data.iloc[0]
    last_point = bollinger_data.iloc[-1]
    assert first_point['upper_bb'] == 918.6978479876341 and first_point['lower_bb'] == 739.9591466123659 and \
           last_point['upper_bb'] == 1132.4838026917355 and last_point['lower_bb'] == 891.1141769082643


def test_sma():
    """
    Tests theSimple Moving Average method against a pre-calculated value.
    """
    trade_intent = common.TradeIntent.SHORT_TRADE
    indicator = common.Indicator.SMA
    window = marketData.get_window(indicator, trade_intent, STOCK_NAME, str(WINDOWS_TEST_JSON_PATH))
    sma_data = marketData.get_SMA(window, STOCK_DATA.loc[:, 'Adj Close']).dropna()
    first_point = sma_data.iloc[0]
    last_point = sma_data.iloc[-1]
    assert first_point == 796.7928552857144 and last_point == 1067.3699775714283


@pytest.mark.xfail
def test_macd():
    """
    Tests the Moving Average Convergence Divergence method against a pre-calculated value.
    """
    trade_intent = common.TradeIntent.SHORT_TRADE
    indicator = common.Indicator.MACD
    window_fast, window_slow, window_sig = marketData.get_window(indicator, trade_intent, STOCK_NAME,
                                                                 str(WINDOWS_TEST_JSON_PATH))
    macd_data = marketData.get_MACD(window_fast, window_slow, window_sig, STOCK_DATA).dropna()
    first_point = macd_data.iloc[0]
    last_point = macd_data.iloc[-1]
    assert first_point['MACD_12_26_9'] == -14.815544928782401 and first_point['MACDh_12_26_9'] == -14.91277246243961 \
           and first_point['MACDs_12_26_9'] == 0.09722753365720867 and last_point['MACD_12_26_9'] == 6.8590096786056165 \
           and last_point['MACDh_12_26_9'] == 11.612237260092115 and last_point['MACDs_12_26_9'] == -4.753227581486499


def test_ema():
    """
    Tests the Exponential Moving Average method against a pre-calculated value.
    """
    trade_intent = common.TradeIntent.SHORT_TRADE
    indicator = common.Indicator.EMA
    window = marketData.get_window(indicator, trade_intent, STOCK_NAME, str(WINDOWS_TEST_JSON_PATH))
    macd_data = marketData.get_EMA(window, STOCK_DATA).dropna()
    first_point = macd_data.iloc[0]
    last_point = macd_data.iloc[-1]
    assert first_point == 796.7928552857144 and last_point == 1053.728121349944


def test_window_data():
    """
    Tests the relative strength Index method against a pre-calculated value.
    """
    trade_intent = common.TradeIntent.SHORT_TRADE
    indicator = common.Indicator.EMA
    window = marketData.get_window(indicator, trade_intent, STOCK_NAME, str(WINDOWS_TEST_JSON_PATH))
    assert window == 7
