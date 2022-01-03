import enum


class TradeIntent(enum.Enum):
    """
    Type of trade intent, whether we want to trade it on a long or short timeframe, or hold.
    """
    UNKNOWN = 0
    LONG_HOLD = 1
    LONG_TRADE = 2
    SHORT_TRADE = 3

    def toString(self):
        return self.name
