from algo_main import api
import time
import datetime
import enum
from datetime import timedelta
from pytz import timezone

tz = timezone('EST')


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


def analyseRSI(name, timeframe):
    """
    RSI analysis of the provided asset based on provided timeframe.\n
    :param name: (string) name of stock
    :param timeframe: (int) interval for the data
    :return: (float) the confidence in the provided asset
    """
    return 1.0


def analyseEMA(name, timeframe):
    """
    EMA analysis of the provided asset based on provided timeframe.\n
    :param name: (string) name of stock
    :param timeframe: (int) interval for the data
    :return: (float) the confidence in the provided asset
    """
    return 1.0


def analyseBollinger(name, timeframe):
    """
    Bollinger analysis of the provided asset based on provided timeframe.\n
    :param name: (string) name of stock
    :param timeframe: (int) interval for the data
    :return: (float) the confidence in the provided asset
    """
    return 1.0


def analyseMACD(name, timeframe):
    """
    MACD analysis of the provided asset based on provided timeframe.\n
    :param name: (string) name of stock
    :param timeframe: (int) interval for the data
    :return: (float) the confidence in the provided asset
    """
    return 1.0


def analyseVolume(name, timeframe):
    """
    Volume analysis of the provided asset based on provided timeframe.\n
    :param name: (string) name of stock
    :param timeframe: (int) interval for the data
    :return: (float) the confidence in the provided asset
    """
    return 1.0


def analyseSMA(name, timeframe):
    """
    SMA analysis of the provided asset based on provided timeframe.\n
    :param name: (string) name of stock
    :param timeframe: (int) interval for the data
    :return: (float) the confidence in the provided asset
    """
    return 1.0


def analyse(stock_name, indicator, timeframe):
    """
    TODO - feed output into ML algorithm. \n
    ------\n
    Simple framework that connects to the corresponding indicator analysis based on the
    :class:`Indicator` type. \n
    :param stock_name: (str) name of asset.
    :param indicator: (enum) indicator name.
    :param timeframe: (int) used to determine the bar-set data intervals.
    :return: (float) confidence of the provided indicator analysis [-1,1] for whether it will increase.
    """
    if indicator == Indicator.RSI:
        return analyseRSI(stock_name, timeframe)
    elif indicator == Indicator.EMA:
        return analyseEMA(stock_name, timeframe)
    elif indicator == Indicator.BOLLINGER:
        return analyseBollinger(stock_name, timeframe)
    elif indicator == Indicator.MACD:
        return analyseMACD(stock_name, timeframe)
    elif indicator == Indicator.VOLUME:
        return analyseVolume(stock_name, timeframe)
    elif indicator == Indicator.SMA:
        return analyseSMA(stock_name, timeframe)
    else:
        print(f"{indicator} is not a valid  or supported Indicator type.")
        return 0.0
