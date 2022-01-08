from pytrader.common.status import Status


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


class ExchangeListener:
    def __init__(self):
        self.__status = Status.INIT

    def listen_for(self):
        pass
