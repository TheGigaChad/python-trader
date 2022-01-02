import enum


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
