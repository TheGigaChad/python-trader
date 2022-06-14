import enum
import logging
import sys
import time
from datetime import datetime

from pytrader.common.indicator import Indicator
from pytrader.common.tradeIntent import TradeIntent
from pytrader.marketData.marketData import analyse

logging.basicConfig(filename='trade.log', format='%(name)s - %(levelname)s - %(message)s')


class Intention(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


def _getIndicators():
    return [Indicator.MACD, Indicator.RSI, Indicator.EMA, Indicator.BOLLINGER, Indicator.SMA, Indicator.VOLUME]


class TradingInstance:
    """
    This is the slave that determines whether a purchase or sale of an asset is a good idea.  These will be spawned by
    the TradingManager and will return a purchase response/
    """

    def __init__(self, name: str, trade_intent: TradeIntent, intention: Intention):
        self.name: str = name
        self.trade_intent: TradeIntent = trade_intent
        self.intention: Intention = intention
        self.model = None
        self.indicator_list: list[Indicator] = _getIndicators()
        self.confidence_buy_threshold: float = 1.0
        self.confidence_sell_threshold: float = 0.0


def getTickerName():
    """
    Determines name based on the parent instantiation. \n
    :return: (string) name / currently defaults to 'TSLA'
    """
    try:
        return sys.argv[1]
    except Exception as e:
        default = 'TSLA'
        logging.error("{} : {}".format(datetime.now().strftime("%x %X"), e))
        print(f"the ticker name was unable to be determined, for now default to {default}")
        return default


def interpretMarket(stock_name: str, trade_intent: TradeIntent, indicator_list: list[Indicator]) -> float:
    """
    This is the container for the market interpretation. \n
    :param stock_name: name of asset.
    :param trade_intent: determines whether we are short/long/hold analysing.
    :param indicator_list: list of indicators we want to use for our interpretation
    :return: confidence value that determines what to do.
    """
    logging.warning(
        '{} : {} started successfully'.format(datetime.now().strftime("%x %X"), stock_name))
    confidence = 0
    for i in indicator_list:
        i_conf = analyse(stock_name, trade_intent, i)
        confidence = confidence + i_conf

    return confidence / len(indicator_list)


def run(instance: TradingInstance):
    """
    main method for each subprocess based on  stock object. \n
    :param instance: instance
    """
    i = 0
    while True:
        confidence = interpretMarket(instance.name, instance.trade_intent, instance.indicator_list)
        if confidence >= instance.confidence_buy_threshold and instance.intention == Intention.BUY:
            print("buy time")
        elif confidence <= instance.confidence_sell_threshold and instance.intention == Intention.SELL:
            print("SELL NOW")
        i = i + 1
        if i > 0:
            break
        time.sleep(1)


# ----------
# main
# ----------
def main():
    """
    main method for the subprocess. \n
    """
    ticker_name = getTickerName()
    instance = TradingInstance(name=ticker_name, trade_intent=TradeIntent.SHORT_TRADE, intention=Intention.SELL)
    run(instance)


# ----------
# Start here
# ----------

main()
