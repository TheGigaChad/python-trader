from typing import Optional

from algo_indicators import Indicator
from algo_tradeIntent import TradeIntent
from algo_position import Position


class Stock:
    """
    Stock class object that holds all the information relevant to the ability to trade the stock effectively
    """

    def __init__(self, ticker_name: str, indicator_list: list[Indicator], trade_intent: TradeIntent,
                 position: Position, indicator_scalar: Optional[float] = 1, buy_threshold: Optional[float] = 1,
                 sell_threshold: Optional[float] = -1, upper_confidence_giveup: Optional[float] = 0.1,
                 lower_confidence_giveup: Optional[float] = -0.1):
        self.ticker_name = ticker_name
        self.indicator_list = indicator_list
        self.EMA_scalar = indicator_scalar
        self.bollinger_scalar = indicator_scalar
        self.RSI_scalar = indicator_scalar
        self.MACD_scalar = indicator_scalar
        self.SMA_scalar = indicator_scalar
        self.trade_intent = trade_intent
        self.position = position
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.upper_confidence_giveup = upper_confidence_giveup
        self.lower_confidence_giveup = lower_confidence_giveup
