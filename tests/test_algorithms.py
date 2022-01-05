import pandas as pd
from algo.algo_tradeIntent import TradeIntent
from marketData import marketData
from algo.algo_indicators import Indicator

stock_name = "TSLA"
stock_data = pd.read_csv("TSLA_historical_data.csv")


def test_RSI():
    trade_intent = TradeIntent.SHORT_TRADE
    indicator = Indicator.RSI
    window = marketData.getWindow(indicator, trade_intent, stock_name, 'test_algo_windows.json')
    rsi_data = marketData.getRSI(window, stock_data).rsi().dropna()
    first_point = rsi_data.iloc[0]
    last_point = rsi_data.iloc[-1]
    assert first_point == 69.87030283020084 and last_point == 56.124583112389


def test_Bollinger():
    trade_intent = TradeIntent.SHORT_TRADE
    indicator = Indicator.BOLLINGER
    window = marketData.getWindow(indicator, trade_intent, stock_name, 'test_algo_windows.json')
    bollinger_data = marketData.appendBollinger(window, stock_data).dropna()
    first_point = bollinger_data.iloc[0]
    last_point = bollinger_data.iloc[-1]
    assert first_point['upper_bb'] == 918.6978479876342 and first_point['lower_bb'] == 739.9591466123658 and \
           last_point['upper_bb'] == 1132.483802691736 and last_point['lower_bb'] == 891.1141769082644


def test_SMA():
    trade_intent = TradeIntent.SHORT_TRADE
    indicator = Indicator.SMA
    window = marketData.getWindow(indicator, trade_intent, stock_name, 'test_algo_windows.json')
    sma_data = marketData.getSMA(window, stock_data.loc[:, 'Adj Close']).dropna()
    first_point = sma_data.iloc[0]
    last_point = sma_data.iloc[-1]
    assert first_point == 796.7928552857144 and last_point == 1067.3699775714285


def test_MACD():
    trade_intent = TradeIntent.SHORT_TRADE
    indicator = Indicator.MACD
    window_fast, window_slow, window_sig = marketData.getWindow(indicator, trade_intent, stock_name,
                                                                'test_algo_windows.json')
    macd_data = marketData.getMACD(window_fast, window_slow, window_sig, stock_data).dropna()
    first_point = macd_data.iloc[0]
    last_point = macd_data.iloc[-1]
    assert first_point['MACD_12_26_9'] == -13.623186637203617 and first_point['MACDh_12_26_9'] == -16.268799961263742 \
           and first_point['MACDs_12_26_9'] == 2.645613324060125 and last_point['MACD_12_26_9'] == 6.859009678606299 \
           and last_point['MACDh_12_26_9'] == 11.61223726009237 and last_point['MACDs_12_26_9'] == -4.753227581486071


def test_EMA():
    trade_intent = TradeIntent.SHORT_TRADE
    indicator = Indicator.EMA
    window = marketData.getWindow(indicator, trade_intent, stock_name, 'test_algo_windows.json')
    macd_data = marketData.getEMA(window, stock_data).dropna()
    first_point = macd_data.iloc[0]
    last_point = macd_data.iloc[-1]
    assert first_point == 796.7928552857144 and last_point == 1053.728121349944


def test_window_data():
    trade_intent = TradeIntent.SHORT_TRADE
    indicator = Indicator.EMA
    window = marketData.getWindow(indicator, trade_intent, stock_name, 'test_algo_windows.json')
    assert window == 7
