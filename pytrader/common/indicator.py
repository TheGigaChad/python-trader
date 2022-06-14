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

    def to_string(self):
        return self.name

    def to_short_string(self) -> str:
        if self.name == self.UNKNOWN.to_string():
            return "UNKNOWN"
        if self.name == self.RSI.to_string():
            return "RSI"
        if self.name == self.EMA.to_string():
            return "EMA"
        if self.name == self.BOLLINGER.to_string():
            return "BOLB"
        if self.name == self.MACD.to_string():
            return "MACD"
        if self.name == self.VOLUME.to_string():
            return "VOL"
        if self.name == self.SMA.to_string():
            return "SMA"
