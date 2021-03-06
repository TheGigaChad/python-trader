import datetime
import json
from datetime import timedelta
from pathlib import Path
from typing import Optional

import pandas
import pandas_ta as pta
import yahoo_fin.stock_info as si
from pytz import timezone
from ta.momentum import RSIIndicator
from ta.volume import on_balance_volume

from pytrader import common
# TODO - REMOVE THIS SHIT
from pytrader.algo.algo_main import api

tz = timezone('EST')

# TODO-ml: We need to be able to determine these scalars
RSI_GRADIENT_SCALAR = 1
RSI_INSTANTANEOUS_SCALAR = 1


def get_window(indicator: common.Indicator, trade_intent: common.TradeIntent, ticker: str,
               file: Optional[str] = Path(__file__).parent.parent / "sql/sqlDb/data/test_algo_windows.json"):
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
        if item["name"] == ticker:
            if indicator == common.Indicator.MACD:
                macd_indicators = ["fast", "slow", "sig"]
                macd_fast = indicator.to_short_string() + "_" + macd_indicators[0] + "_" + trade_intent.value.lower()
                macd_slow = indicator.to_short_string() + "_" + macd_indicators[1] + "_" + trade_intent.value.lower()
                macd_sig = indicator.to_short_string() + "_" + macd_indicators[2] + "_" + trade_intent.value.lower()
                return item[macd_fast], item[macd_slow], item[macd_sig]
            else:
                sql_column_name = indicator.to_short_string() + "_" + trade_intent.value.lower()
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


def time_to_open(current_time: datetime) -> float:
    """
    Returns how long until the markets are open, this is not useful for crypto and other 24/7 markets. \n
    :param current_time: current time.
    :return: seconds until the markets open.
    """
    if current_time.weekday() <= 4:
        d = (current_time + timedelta(days=1)).date()
    else:
        days_to_mon = 0 - current_time.weekday() + 7
        d = (current_time + timedelta(days=days_to_mon)).date()
    next_day = datetime.datetime.combine(d, datetime.time(9, 30, tzinfo=tz))
    seconds = (next_day - current_time).total_seconds()
    return seconds


def get_RSI(window: int, data: pandas.DataFrame) -> pandas.Series:
    """
    RSI data of the provided asset based on provided timeframe.\n
    :param window: time frame of analysis
    :param data: yahoo-fin stock object relating to stock.
    :return: RSI data
    """
    if data.columns.__contains__("adjclose"):
        data.rename(columns={"adjclose": "Adj Close"}, inplace=True)
    return RSIIndicator(close=data['Adj Close'], window=window).rsi()


def analyse_RSI(trade_intent: common.TradeIntent, data: pandas.DataFrame, ticker: str) -> float:
    """
    RSI analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: determines whether we are short/long/hold analysing.
    :param data: stock data.
    :param ticker: name of stock.
    :return: the confidence in the provided asset.
    """
    window = get_window(common.Indicator.RSI, trade_intent, ticker)
    rsi_data = get_RSI(window, data)

    if rsi_data is None:
        print("analyseRSI - momentum RSI data is none")
        return 0.0

    # Scale the RSI to be between -3,3 to fit tanh scale, then return tanh to go a value between -1,1
    # rsi_scaled = (0.06 * rsi_data.rsi()) - 3
    #
    # # Because RSI is inverted (high rsi, we want to sell) we invert the result
    # rsi_tanh = math.tanh(rsi_scaled) * -1
    #
    # # Gradient calculations
    # data_y = np.array(data)
    # data_x = np.arange(1, len(data_y) + 1)
    # # Fit line
    # slope, intercept = np.polyfit(data_x, data_y, 1)
    #
    # # rescale gradient, accommodate for inverse in the same way rsi value is
    # slope_scaled = (window / 100) * slope
    # slope_tanh = math.tanh(slope_scaled) * -1
    #
    # rsi_out = (slope_tanh * RSI_GRADIENT_SCALAR) + (rsi_tanh * RSI_INSTANTANEOUS_SCALAR) / 2
    return 1.0


def get_EMA(window: int, data: pandas.DataFrame) -> pandas.Series:
    """
    EMA data of the provided asset based on provided timeframe.\n
    :param window: time frame of analysis
    :param data: stock data
    :return: (pandas.Series) EMA data
    """
    if data.columns.__contains__("adjclose"):
        data.rename(columns={"adjclose": "Adj Close"}, inplace=True)
    ema_data = pta.ema(close=data['Adj Close'], length=window)
    return ema_data


def analyse_EMA(trade_intent: common.TradeIntent, data: pandas.DataFrame, ticker: str) -> float:
    """
    EMA analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: determines whether we are short/long/hold analysing.
    :param data: data set
    :param ticker: name of stock
    :return: the confidence in the provided asset
    """
    window = get_window(common.Indicator.EMA, trade_intent, ticker)
    ema_data = get_EMA(window, data)
    return 1.0


def bollinger_bounds(data: pandas.DataFrame, sma: pandas.Series, window: int):
    """"
    Determines the upper and lower bounds for the bollinger bands
    :param data: stock data
    :param sma: simple moving average data
    :param window: time frame of analysis
    """
    std = data.rolling(window=window).std()
    upper_bb = sma + std * 2
    lower_bb = sma - std * 2
    return upper_bb, lower_bb


def append_bollinger(window: int, data: pandas.DataFrame) -> pandas.DataFrame:
    """
    Appends Bollinger data to dataframe.
    :param window: time frame of analysis
    :param data: yahoo-fin stock object relating to stock.
    :return: updated data frame
    """
    sma_name = "sma_" + str(window)
    data[sma_name] = get_SMA(window, data)
    if data.columns.__contains__("adjclose"):
        data.rename(columns={"adjclose": "Adj Close"}, inplace=True)
    data['upper_bb'], data['lower_bb'] = bollinger_bounds(data['Adj Close'], data[sma_name], window)
    return data


def analyse_bollinger(trade_intent: common.TradeIntent, data: pandas.DataFrame, ticker: str) -> float:
    """
    Bollinger analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: determines whether we are short/long/hold analysing.
    :param data: stock data
    :param ticker: name of stock
    :return: the confidence in the provided asset
    """
    window = get_window(common.Indicator.BOLLINGER, trade_intent, ticker)
    bollinger_data = append_bollinger(window, data)
    return 1.0


def get_MACD(window_fast: int, window_slow: int, window_sig: int, data: pandas.DataFrame) -> pandas.DataFrame:
    """
    MACD analysis of the provided asset based on provided timeframe.\n
    :param window_fast: fast moving window
    :param window_slow: slow moving window
    :param window_sig: signal window
    :param data: stock data
    :return: MACD data
    """
    if data.columns.__contains__("adjclose"):
        data.rename(columns={"adjclose": "Adj Close"}, inplace=True)

    macd_data = pta.macd(close=data['Adj Close'], fast=window_fast, slow=window_slow, signal=window_sig, append=True)
    return macd_data


def analyse_MACD(trade_intent: common.TradeIntent, data: pandas.DataFrame, ticker: str) -> float:
    """
    MACD analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: determines whether we are short/long/hold analysing.
    :param data: stock data
    :param ticker: name of stock
    :return: the confidence in the provided asset
    """
    window_fast, window_slow, window_sig = get_window(common.Indicator.MACD, trade_intent, ticker)
    macd_data = get_MACD(window_fast, window_slow, window_sig, data)
    return 1.0


def analyse_volume(trade_intent: common.TradeIntent, data: pandas.DataFrame, ticker: str) -> float:
    """
    Volume analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: determines whether we are short/long/hold analysing.
    :param data: stock data
    :param ticker: name of stock
    :return: the confidence in the provided asset
    """
    window = get_window(common.Indicator.VOLUME, trade_intent, ticker)
    volume_data = on_balance_volume(close=data.adjclose, volume=data.volume)

    if volume_data is None:
        print("analyseVolume - volume data is null")
        return 0.0

    return 1.0


def get_SMA(window: int, data: pandas.DataFrame) -> pandas.Series:
    """
    Simple Moving Average for given window and data.\n
    :param window: interval window.
    :param data: historical data of stock.
    :return: Simple Moving Average Array
    """
    if isinstance(data, pandas.DataFrame):
        if data.columns.__contains__("adjclose"):
            data.rename(columns={"adjclose": "Adj Close"}, inplace=True)
        data = data.loc[:, 'Adj Close']
    sma = data.rolling(window=window).mean()
    return sma


def analyse_SMA(trade_intent: common.TradeIntent, data: pandas.DataFrame, ticker: str) -> float:
    """
    SMA analysis of the provided asset based on provided timeframe.\n
    :param trade_intent: determines whether we are short/long/hold analysing.
    :param data: stock data
    :param ticker: name of stock
    :return: the confidence in the provided asset
    """
    window = get_window(common.Indicator.SMA, trade_intent, ticker)
    sma = get_SMA(window, data.adjclose)
    return 1.0


def analyse(stock_name: str, trade_intent: common.TradeIntent, indicator: common.Indicator) -> float:
    """
    TODO - feed output into ml algorithm. \n
    ------\n
    Simple framework that connects to the corresponding indicator analysis
    :param stock_name: name of asset.
    :param trade_intent: determines whether we are short/long/hold analysing.
    :param indicator: indicator name.
    :return: confidence of the provided indicator analysis [-1,1] for whether it will increase.
    """
    data = si.get_data(str(stock_name))

    if indicator == common.Indicator.RSI:
        return analyse_RSI(trade_intent, data, stock_name)
    elif indicator == common.Indicator.EMA:
        return analyse_EMA(trade_intent, data, stock_name)
    elif indicator == common.Indicator.BOLLINGER:
        return analyse_bollinger(trade_intent, data, stock_name)
    elif indicator == common.Indicator.MACD:
        return analyse_MACD(trade_intent, data, stock_name)
    elif indicator == common.Indicator.VOLUME:
        return analyse_volume(trade_intent, data, stock_name)
    elif indicator == common.Indicator.SMA:
        return analyse_SMA(trade_intent, data, stock_name)

    else:
        print(f"{indicator} is not a valid  or supported Indicator type.")
        return 0.0
