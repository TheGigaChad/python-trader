class SQLDbWindowsDao:
    """
    dao  that handles the window from the sql response.
    """

    def __init__(self, name: str, sma_short_trade: int, sma_long_trade: int, sma_long_hold: int, ema_short_trade: int,
                 ema_long_trade: int, ema_long_hold: int, macd_fast_short_trade: int, macd_slow_short_trade: int,
                 macd_sig_short_trade: int, macd_fast_long_trade: int, macd_slow_long_trade: int,
                 macd_sig_long_trade: int,
                 macd_fast_long_hold: int, macd_slow_long_hold: int, macd_sig_long_hold: int, rsi_short_trade: int,
                 rsi_long_trade: int, rsi_long_hold: int, vol_short_trade: int, vol_long_trade: int, vol_long_hold: int,
                 bolb_short_trade: int, bolb_long_trade: int, bolb_long_hold: int):
        self.__name: str = name
        self.__sma_short_trade: int = sma_short_trade
        self.__sma_long_trade: int = sma_long_trade
        self.__sma_long_hold: int = sma_long_hold
        self.__ema_short_trade: int = ema_short_trade
        self.__ema_long_trade: int = ema_long_trade
        self.__ema_long_hold: int = ema_long_hold
        self.__macd_fast_short_trade: int = macd_fast_short_trade
        self.__macd_slow_short_trade: int = macd_slow_short_trade
        self.__macd_sig_short_trade: int = macd_sig_short_trade
        self.__macd_fast_long_trade: int = macd_fast_long_trade
        self.__macd_slow_long_trade: int = macd_slow_long_trade
        self.__macd_sig_long_trade: int = macd_sig_long_trade
        self.__macd_fast_long_hold: int = macd_fast_long_hold
        self.__macd_slow_long_hold: int = macd_slow_long_hold
        self.__macd_sig_long_hold: int = macd_sig_long_hold
        self.__rsi_short_trade: int = rsi_short_trade
        self.__rsi_long_trade: int = rsi_long_trade
        self.__rsi_long_hold: int = rsi_long_hold
        self.__vol_short_trade: int = vol_short_trade
        self.__vol_long_trade: int = vol_long_trade
        self.__vol_long_hold: int = vol_long_hold
        self.__bolb_short_trade: int = bolb_short_trade
        self.__bolb_long_trade: int = bolb_long_trade
        self.__bolb_long_hold: int = bolb_long_hold

    @property
    def name(self):
        return self.__name

    @property
    def sma_short_trade(self):
        return self.__sma_short_trade

    @property
    def sma_long_trade(self):
        return self.__sma_long_trade

    @property
    def sma_long_hold(self):
        return self.__sma_long_hold

    @property
    def ema_short_trade(self):
        return self.__ema_short_trade

    @property
    def ema_long_trade(self):
        return self.__ema_long_trade

    @property
    def ema_long_hold(self):
        return self.__ema_long_hold

    @property
    def macd_fast_short_trade(self):
        return self.__macd_fast_short_trade

    @property
    def macd_slow_short_trade(self):
        return self.__macd_slow_short_trade

    @property
    def macd_sig_short_trade(self):
        return self.__macd_sig_short_trade

    @property
    def macd_fast_long_trade(self):
        return self.__macd_fast_long_trade

    @property
    def macd_slow_long_trade(self):
        return self.__macd_slow_long_trade

    @property
    def macd_sig_long_trade(self):
        return self.__macd_sig_long_trade

    @property
    def macd_fast_long_hold(self):
        return self.__macd_fast_long_hold

    @property
    def macd_slow_long_hold(self):
        return self.__macd_slow_long_hold

    @property
    def macd_sig_long_hold(self):
        return self.__macd_sig_long_hold

    @property
    def rsi_short_trade(self):
        return self.__rsi_short_trade

    @property
    def rsi_long_trade(self):
        return self.__rsi_long_trade

    @property
    def rsi_long_hold(self):
        return self.__rsi_long_hold

    @property
    def vol_short_trade(self):
        return self.__vol_short_trade

    @property
    def vol_long_trade(self):
        return self.__vol_long_trade

    @property
    def vol_long_hold(self):
        return self.__vol_long_hold

    @property
    def bolb_short_trade(self):
        return self.__bolb_short_trade

    @property
    def bolb_long_trade(self):
        return self.__bolb_long_trade

    @property
    def bolb_long_hold(self):
        return self.__bolb_long_hold
