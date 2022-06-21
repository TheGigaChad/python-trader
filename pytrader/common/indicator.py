import enum


class Indicator(str, enum.Enum):
    """
    Enum that distinguishes the type of indicator (RSI, EMA...).
    """
    UNKNOWN = 'unknown'
    RSI = 'rsi'
    EMA = 'ema'
    BOLLINGER = 'bollinger'
    MACD = 'macd'
    VOLUME = 'volume'
    SMA = 'sma'

    def to_string(self):
        return self.name

    def to_short_string(self) -> str:
        if self.name == self.UNKNOWN.to_string():
            return "unknown"
        if self.name == self.RSI.to_string():
            return "rsi"
        if self.name == self.EMA.to_string():
            return "ema"
        if self.name == self.BOLLINGER.to_string():
            return "bolb"
        if self.name == self.MACD.to_string():
            return "macd"
        if self.name == self.VOLUME.to_string():
            return "vol"
        if self.name == self.SMA.to_string():
            return "sma"
