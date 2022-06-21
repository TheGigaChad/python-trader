import enum


class TradeIntent(enum.Enum):
    """
    Type of trade intent, whether we want to trade it on a long or short timeframe, or hold.
    """
    UNKNOWN = "UNKNOWN"
    LONG_HOLD = "LONG_HOLD"
    LONG_TRADE = "LONG_TRADE"
    SHORT_TRADE = "SHORT_TRADE"
