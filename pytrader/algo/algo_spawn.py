import sys
import logging
import datetime
from algo_main import api
from pytrader.config import ALPACA_PAPER_KEY, ALPACA_PAPER_SECRET
from algo_stock import Stock
import time
import random
import websocket
import json
from pytrader.marketData.marketData import analyse
from algo_indicators import Indicator
from algo_tradeIntent import TradeIntent
from algo_position import Position

logging.basicConfig(filename='algo.log', format='%(name)s - %(levelname)s - %(message)s')


def return_trade_rating():
    """
    TODO \n
    :return: 1 at the moment
    """
    return 1


def getTickerName():
    """
    Determines name based on the parent instantiation. \n
    :return: (string) name / currently defaults to 'TSLA'
    """
    try:
        return sys.argv[1]
    except Exception as e:
        default = 'TSLA'
        print(f"the ticker name was unable to be determined, for now default to {default}")
        return default


def getDebugMode():
    """
    Determines whether we are in debug mode based on arguments passed. \n
    :return: (boolean) debug mode
    """
    try:
        name = sys.argv[1]
        return False
    except Exception as e:
        print("debug mode activated")
        return True


def purchaseSuccessful(order_id):
    """
    returns true if exchange fills trade, else false if cancelled or timed out. \n
    :param order_id: id of trade.
    """
    timer = 0
    time_increment = 0.2
    time_max = 10
    while timer <= time_max:
        print(f"status is: {api.get_order_by_client_order_id(order_id).status}")
        if api.get_order_by_client_order_id(order_id).status == 'filled':
            return True
        else:
            timer = timer + time_increment
            time.sleep(time_increment)
    return False


def buy(stock, allowance):
    """
    The buy method for a :class:`Stock`. \n
    :param stock: (Stock) object
    :param allowance: (float) quantity
    :return: nothing yet?
    """
    try:
        current_price = api.get_barset(stock.ticker_name, 'minute', limit=1)[stock.ticker_name][0].h
        print(f"current price is: {current_price}")
        qty = int(allowance / float(current_price))
        print(f"buying quantity: {qty}")
        if qty <= 0:
            logging.warning('{} : {} insufficient funds to buy {} stock(s)'.format
                            (datetime.datetime.now().strftime("%x %X"), stock.ticker_name, qty))
            return
        order_id = str(random.randrange(1, 10000000))
        print(f"buying..")
        # listenForTradeUpdate(order_id, stock.ticker_name, qty, order_id)
        api.submit_order(symbol=stock.ticker_name,
                         qty=qty,
                         side='buy',
                         type='market',
                         client_order_id=order_id)
        print(api.get_order_by_client_order_id(order_id).status)
        t = purchaseSuccessful(order_id)
        if t:
            stock.position = Position.TRADING
            print("successful")
        else:
            print("retrying buy attempt, cancelling original trade")
            api.cancel_order(order_id)
            buy(stock, allowance)
        print("buy offer successfully received by exchange.")
        logging.warning(
            '{} : bought {} stock(s) of {}'.format(datetime.datetime.now().strftime("%x %X"), qty, stock.ticker_name))
    except Exception as e:
        logging.error(
            '{} : unable to buy {}. {}'.format(datetime.datetime.now().strftime("%x %X"), stock.ticker_name, e))


def sell(stock, q):
    """
    The sell method for a :class:`Stock`. \n
    :param stock: (Stock) object
    :param q: (float) quantity
    :return: nothing yet?
    """
    try:
        order_id = str(random.randrange(1, 10000000))
        api.submit_order(symbol=stock.ticker_name,
                         qty=q,
                         side='sell',
                         type='market',
                         client_order_id=order_id)
        stock.position = Position.TRADING
        # listenForTradeUpdate(order_id)
        logging.warning(
            '{} : sold {} stock(s) of  {}'.format(datetime.datetime.now().strftime("%x %X"), q, stock.ticker_name))
    except Exception as e:
        logging.error(
            '{} : unable to sell {}. {}'.format(datetime.datetime.now().strftime("%x %X"), stock.ticker_name, e))
        pass


def request_selloff():
    """
    TODO \n
    Special method that requests to the parent process that the buy params are very
    profitable and requests extra allowance. \n
    :return: Nothing yet
    """
    pass


def requestAllowance(stock, confidence):
    """
    TODO - needs some bulletproofing... \n
    -------- \n
    Requests an allotted allowance in order to make a purchase.  Currently it prints for master to hear \n
    :return: Nothing
    """
    logging.warning(
        '{} : {} requesting allowance'.format(datetime.datetime.now().strftime("%x %X"), stock))
    if sys.stdout.writable():
        sys.stdout.write(f"ALLOWANCE~{stock}~{confidence}\n")
    time.sleep(5)
    try:
        s = sys.stdin.readline()
        if type(s) is type(str) and len(s) > 0:
            return float(s)
    except Exception as e:
        logging.warning(
            '{} : {} decode error {}'.format(datetime.datetime.now().strftime("%x %X"), stock, e))
        pass
    finally:
        logging.warning(
            '{} funding of {} received for {}'.format(datetime.datetime.now().strftime("%x %X"), (s),
                                                      stock))


def getInitialPosition(ticker_name: str) -> Position:
    """
    Determines whether we own the stock or whether we have an active trade and returns the position type \n
    :param ticker_name: name of stock
    :return: the position
    """
    open_orders = api.list_orders(
        status='open',
        limit=100,
        nested=True  # show nested multi-leg orders
    )
    open_order_list = [o for o in open_orders if o.symbol == ticker_name]
    if len(open_order_list) > 0:
        return Position.TRADING

    positions = api.list_positions()
    for stock in positions:
        if stock.symbol == ticker_name:
            return Position.OWNED

    return Position.UNOWNED


def getTradeIntent() -> TradeIntent:
    # TODO - this needs to be in an SQL table
    """
    Determines the trade intent type \n
    :return: trade intent
    """
    return TradeIntent.SHORT_TRADE


def on_open(ws):
    """
    on_open callback from :class:`websocket.WebSocketApp`. \n
    :param ws: websocket
    """
    print("opening socket")
    auth_data = {
        "action": "authenticate",
        "data": {
            "key_id": ALPACA_PAPER_KEY,
            "secret_key": ALPACA_PAPER_SECRET}
    }
    ws.send(json.dumps(auth_data))
    channel_data = {
        "action": "listen",
        "data": {
            "streams": ["trade_updates"]
        }
    }
    ws.send(json.dumps(channel_data))


def on_message(ws, message):
    """
    on_message callback from :class:`websocket.WebSocketApp`. \n
    :param ws: websocket
    :param message: message
    """
    print(message)


def listenForTradeUpdate(name, qty, id):
    """
    Once a buy or sell request has been made, we listen to make sure it is successful. \n
    :param trade_id: (string) id of the relevant trade
    :return: (boolean) true/false whether trade was successful
    """
    stream = "wss://paper-api.alpaca.markets/stream"
    try:
        ws = websocket.WebSocketApp(stream, on_open=on_open, on_message=on_message)
        print(ws)
        api.submit_order(symbol=name,
                         qty=qty,
                         side='buy',
                         type='market',
                         client_order_id=id)

        # ws.run_forever()
    except Exception as e:
        print(e)
    return True


def getStockPrice(ticker_name):
    """
    Gets the current price of the :class:`Stock`. \n
    :param ticker_name: (string) name of stock
    :return: (int) price
    """
    try:
        return api.get_last_quote(ticker_name)
    except Exception as e:
        print(e)


def interpretMarket(stock_name: str, trade_intent: TradeIntent, indicator_list: list[Indicator]) -> float:
    """
    This is the container for the market interpretation. \n
    :param stock_name: name of asset.
    :param trade_intent: determines whether we are short/long/hold analysing.
    :param indicator_list: list of indicators we want to use for our interpretation
    :return: confidence value that determines what to do.
    """
    logging.warning(
        '{} : {} started successfully'.format(datetime.datetime.now().strftime("%x %X"), stock_name))
    confidence = 0
    for i in indicator_list:
        i_conf = analyse(stock_name, trade_intent, i)
        confidence = confidence + i_conf

    return confidence


def run(stock: Stock):
    """
    main method for each subprocess based on  stock object. \n
    :param stock: Stock object
    """
    i = 0
    j = random.randrange(1, 4)
    while True:
        try:
            confidence = interpretMarket(stock.ticker_name, stock.trade_intent,
                                         stock.indicator_list)

            if stock.lower_confidence_giveup <= confidence <= stock.upper_confidence_giveup or i > j:
                break

            elif confidence >= stock.buy_threshold:
                allowance = 10000
                # allowance = requestAllowance(stock.ticker_name, confidence * random.randrange(1, 1000) / 1000)
                buy(stock, allowance)

            elif confidence <= stock.sell_threshold and stock.position == Position.OWNED:
                sell(stock, 1)
                pass
            i = i + 1
            time.sleep(10000)
        except Exception as e:
            logging.warning(
                '{} : {} subprocess crashed -  {}'.format(datetime.datetime.now().strftime("%x %X"), stock.ticker_name,
                                                          e))


def quitting(name: str):
    """
    Tidy up works on the quitting of subprocess. \n
    :param name:  ticker name
    """
    logging.warning('{} : {} subprocess closed successfully.'.format(datetime.datetime.now().strftime("%x %X"), name))
    print("quit")


# ----------
# main
# ----------
def main():
    """
    main method for the subprocess. \n
    """
    debug_mode = getDebugMode()
    ticker_name = getTickerName()
    indicator_list = [Indicator.MACD, Indicator.RSI]
    trade_intent = getTradeIntent()
    position = getInitialPosition(ticker_name)
    stock = Stock(ticker_name, indicator_list, trade_intent, position)
    if not debug_mode:
        run(stock)
    quitting(stock.ticker_name)


# ----------
# Start here
# ----------

main()
