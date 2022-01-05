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

    def toString(self):
        return self.name

    def toShortString(self) -> str:
        if self.name == self.UNKNOWN.toString():
            return "UNKNOWN"
        if self.name == self.RSI.toString():
            return "RSI"
        if self.name == self.EMA.toString():
            return "EMA"
        if self.name == self.BOLLINGER.toString():
            return "BOLB"
        if self.name == self.MACD.toString():
            return "MACD"
        if self.name == self.VOLUME.toString():
            return "VOL"
        if self.name == self.SMA.toString():
            return "SMA"
