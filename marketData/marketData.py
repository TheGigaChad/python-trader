import datetime
import enum
import math
from datetime import timedelta

import numpy as np
import pandas
import json
import yahoo_fin.stock_info as si
from pytz import timezone
from ta.momentum import RSIIndicator
from ta.volume import on_balance_volume
import pandas_ta as pta

from algo.algo_main import api

tz = timezone('EST')

# TODO-ML: We need to be able to determine these scalars
RSI_GRADIENT_SCALAR = 1
RSI_INSTANTANEOUS_SCALAR = 1


class Indicator(str, enum.Enum):
    """
    Enum that distinguishes the type of indicator (RSI, EMA...).
    """
    UNKNOWN = 'UNKNOWN'
    RSI = 'RSI'
    EMA = 'EMA'
    BOLLINGER = 'BOLLINGER'
    MACD = 'MACD'
    VOLUME = 'VOLUME'
    SMA = 'SMA'


def getWindow(indicator, trade_intent, ticker, file="algo_windows.json"):
    """
    gets the window for analysis. \n
    :param indicator: (Indicator) type of indicator used for analysis.
    :param trade_intent: (TradeIntent) intended trade type (short,long,hold)
    :param file: (file) optional file input override for testing.
    :param ticker: (str) name of ticker.
    :return: (int) window value
    """
    # TODO - add default type
    # TODO - bullet proof MACD option
    json_file = open(file)
    json_data = json.load(json_file)
    json_file.close()
    for item in json_data:
        if item["NAME"] == ticker:
            if indicator == Indicator.MACD:
                macd_indicators = ["FAST", "SLOW", "SIG"]
                macd_fast = indicator.toShortString() + "_" + macd_indicators[0] + "_" + trade_intent.toString()
                macd_slow = indicator.toShortString() + "_" + macd_indicators[1] + "_" + trade_intent.toString()
                macd_sig = indicator.toShortString() + "_" + macd_indicators[2] + "_" + trade_intent.toString()
                return item[macd_fast], item[macd_slow], item[macd_sig]
            else:
                sql_column_name = indicator.toShortString() + "_" + trade_intent.toString()
                return item[sql_column_name]

    print(f"getWindow could not determine the Trade Intent {trade_intent} for the indicator {indicator}")
    return 0



def get_data_bars(symbols, rate, slow, fast):
    data = api.get_barset(symbols, rate, limit=20).df
    for x in symbols:
        data.loc[:, (x, 'fast_ema')] = data[x]['close'].rolling(window=fast).mean()
        data.loc[:, (x, 'slow_ema')] = data[x]['close'].rolling(window=slow).mean()
    return data


def get_signal_bars(symbol_list, rate, ema_slow, ema_fast):
    data = get_data_bars(symbol_list, rate, ema_slow, ema_fast)
    signals = {}
    for x in symbol_list:
        if data[x].iloc[-1]['fast_ema'] > data[x].iloc[-1]['slow_ema']:
            signal = 1
        else:
            signal = 0
        signals[x] = signal
    return signals


def time_to_open(current_time):
    """
    Returns how long until the markets are open, this is useful only for STOCKS. \n
    :param current_time: (time) current time.
    :return: (int) seconds until the markets open.
    """
    if current_time.weekday() <= 4:
        d = (current_time + timedelta(days=1)).date()
    else:
        days_to_mon = 0 - current_time.weekday() + 7
        d = (current_time + timedelta(days=days_to_mon)).date()
    next_day = datetime.datetime.combine(d, datetime.time(9, 30, tzinfo=tz))
    seconds = (next_day - current_time).total_seconds()
    return seconds


def getRSI(window, data):
    """
    RSI data of the provided asset based on provided timeframe.\n
    :param window: (int) time frame of analysis
    :param data: (obj) yahoo-fin stock object relating to stock.
    :return: (pandas.Series) RSI data
    """
    return RSIIndicator(close=data['Adj Close'], window=window)


def analyseRSI(trade_intent, data, ticker):
    """
    RSI analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: (TradeIntent) determines whether we are short/long/hold analysing.
    :param data: (pandas.DataFrame) yahoo-fin stock object relating to stock.
    :param ticker: (str) name of stock
    :return: (float) the confidence in the provided asset
    """
    window = getWindow(Indicator.RSI, trade_intent, ticker)
    rsi_data = getRSI(window, data)

    if rsi_data is None:
        print("analyseRSI - momentum RSI data is none")
        return 0

    # Scale the RSI to be between -3,3 to fit tanh scale, then return tanh to go a value between -1,1
    rsi_scaled = (0.06 * rsi_data.rsi()) - 3

    # Because RSI is inverted (high rsi, we want to sell) we invert the result
    rsi_tanh = math.tanh(rsi_scaled) * -1

    # Gradient calculations
    data_y = np.array(data)
    data_x = np.arange(1, len(data_y) + 1)
    # Fit line
    slope, intercept = np.polyfit(data_x, data_y, 1)

    # rescale gradient, accommodate for inverse in the same way rsi value is
    slope_scaled = (trade_intent / 100) * slope
    slope_tanh = math.tanh(slope_scaled) * -1

    rsi_out = (slope_tanh * RSI_GRADIENT_SCALAR) + (rsi_tanh * RSI_INSTANTANEOUS_SCALAR) / 2
    return rsi_out


def getEMA(window, data):
    """
    EMA data of the provided asset based on provided timeframe.\n
    :param window: (int) time frame of analysis
    :param data: (pandas.DataFrame) yahoo-fin stock object relating to stock.
    :return: (pandas.Series) EMA data
    """
    ema_data = pta.ema(close=data['Adj Close'], length=window)
    return ema_data


def analyseEMA(trade_intent, data, ticker):
    """
    EMA analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: (TradeIntent) determines whether we are short/long/hold analysing.
    :param data: (pandas.DataFrame) data set
    :param ticker: (str) name of stock
    :return: (float) the confidence in the provided asset
    """
    window = getWindow(Indicator.EMA, trade_intent, ticker)
    ema_data = getEMA(window, data)
    return 1.0


def bollingerBounds(data, sma, window):
    """"

    """
    std = data.rolling(window=window).std()
    upper_bb = sma + std * 2
    lower_bb = sma - std * 2
    return upper_bb, lower_bb


def appendBollinger(window, data):
    """
    Appends Bollinger data to dataframe.
    :param window: (int) time frame of analysis
    :param data: (obj) yahoo-fin stock object relating to stock.
    :return: (dataframe) updated data frame
    """
    sma_name = "sma_" + str(window)
    data[sma_name] = getSMA(window, data)
    data['upper_bb'], data['lower_bb'] = bollingerBounds(data['Adj Close'], data[sma_name], window)
    return data


def analyseBollinger(trade_intent, data, ticker):
    """
    Bollinger analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: (TradeIntent) determines whether we are short/long/hold analysing.
    :param data: (data) historical data of stock
    :param ticker: (str) name of stock
    :return: (float) the confidence in the provided asset
    """
    window = getWindow(Indicator.BOLLINGER, trade_intent, ticker)
    bollinger_data = appendBollinger(window, data)

    return 1.0


def getMACD(window_fast, window_slow, window_sig, data):
    """
    MACD analysis of the provided asset based on provided timeframe.\n
    :param window_fast: (int) fast moving window
    :param window_slow: (int) slow moving window
    :param window_sig: (int) signal window
    :param data: (pandas.Dataframe) stock data
    :return: (pandas.Series) MACD data
    """
    macd_data = pta.macd(close=data['Adj Close'], fast=window_fast, slow=window_slow, signal=window_sig, append=True)
    return macd_data


def analyseMACD(trade_intent, data):
    """
    MACD analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: (TradeIntent) determines whether we are short/long/hold analysing.
    :param data: (pandas.Dataframe) stock data
    :return: (float) the confidence in the provided asset
    """
    window_fast, window_slow, window_sig = getWindow(Indicator.MACD, trade_intent)
    macd_data = getMACD(window_fast, window_slow, window_sig, data)
    return 1.0


def analyseVolume(trade_intent, data, ticker):
    """
    Volume analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: (TradeIntent) determines whether we are short/long/hold analysing.
    :param data: (obj) yahoo-fin stock object relating to stock.
    :param ticker: (str) name of stock
    :return: (float) the confidence in the provided asset
    """
    window = getWindow(Indicator.VOLUME, trade_intent, ticker)
    volume_data = on_balance_volume(close=data.adjclose, volume=data.volume)

    if volume_data.isnull:
        print("analyseRSI - momentum RSI data is null")
        return 0

    volume_mean = volume_data.mean()
    volume_current = volume_data.last()

    # Using this.. https://math.stackexchange.com/questions/3425798/how-to-squish-and-squash-x-axis-hyperbolic-tangent
    # We scale the tanh based on stuff
    vol_tanh = 0.5 * (1 - math.tanh(volume_mean * (volume_current - volume_mean)))

    return vol_tanh


def getSMA(window, data):
    """
    Simple Moving Average for given window and data.\n
    :param window: (int) interval window.
    :param data: (data) historical data of stock.
    :return: (array) Simple Moving Average Array
    """
    if isinstance(data, pandas.DataFrame):
        data = data.loc[:, 'Adj Close']
    sma = data.rolling(window=window).mean()
    return sma


def analyseSMA(trade_intent, data, ticker):
    """
    SMA analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: (TradeIntent) determines whether we are short/long/hold analysing.
    :param data: (data) historical data of stock.
    :param ticker: (str) name of stock
    :return: (float) the confidence in the provided asset
    """
    window = getWindow(Indicator.SMA, trade_intent, ticker)
    sma = getSMA(window, data.adjclose)
    return sma


def analyse(stock_name, trade_intent, indicator):
    """
    TODO - feed output into ML algorithm. \n
    ------\n
    Simple framework that connects to the corresponding indicator analysis
    :class:`Indicator` type. \n
    :param stock_name: (str) name of asset.
    :param trade_intent: (TradeIntent) determines whether we are short/long/hold analysing.
    :param indicator: (enum) indicator name.
    :return: (float) confidence of the provided indicator analysis [-1,1] for whether it will increase.
    """
    data = si.get_data(str(stock_name))

    if indicator == Indicator.RSI:
        # return analyseRSI(trade_intent, data)
        return 1
    elif indicator == Indicator.EMA:
        # return analyseEMA(trade_intent, data)
        return 1
    elif indicator == Indicator.BOLLINGER:
        # return analyseBollinger(trade_intent, data)
        return 1
    elif indicator == Indicator.MACD:
        # return analyseMACD(trade_intent, data)
        return 1
    elif indicator == Indicator.VOLUME:
        # return analyseVolume(trade_intent, data)
        return 1
    elif indicator == Indicator.SMA:
        # return analyseSMA(trade_intent, data)
        return 1

    else:
        print(f"{indicator} is not a valid  or supported Indicator type.")
        return 0.0
