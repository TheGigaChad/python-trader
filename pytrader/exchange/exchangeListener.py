import json

import websocket

from pytrader.common.log import Log
from pytrader.common.requests import ResponseStatus
from pytrader.common.status import Status
from pytrader.exchange.exchange import Exchange

Log = Log(__file__)


def listen_for_trade_update(name, qty, id):
    """
    Once a buy or sell request has been made, we listen to make sure it is successful. \n
    :param trade_id: (string) id of the relevant trade
    :return: (boolean) true/false whether trade was successful
    """
    stream = "wss://paper-api.alpaca.markets/stream"
    try:
        pass
        # ws = websocket.WebSocketApp(stream, on_open=on_open, on_message=on_message)
        # print(ws)
        # api.submit_order(symbol=name,
        #                  qty=qty,
        #                  side='buy',
        #                  type='market',
        #                  client_order_id=id)

        # ws.run_forever()
    except Exception as e:
        print(e)
    return True


class ExchangeListener:
    """
    Handles the management of the response from exchanges regarding whether the request was successful.
    """

    def __init__(self):
        self.__status: Status = Status.INIT
        self.__key: str = ""
        self.__secret: str = ""

    def on_open(self, ws):
        """
        on_open callback from :class:`websocket.WebSocketApp`. \n
        :param ws: websocket
        """
        auth_data = {
            "action": "authenticate",
            "data": {
                "key_id": self.__key,
                "secret_key": self.__secret}
        }
        ws.send(json.dumps(auth_data))
        channel_data = {
            "action": "listen",
            "data": {
                "streams": ["trade_updates"]
            }
        }
        ws.send(json.dumps(channel_data))

    def on_message(self, ws: websocket.WebSocketApp, message):
        """
        on_message callback from :class:`websocket.WebSocketApp`. \n
        :param ws: websocket
        :param message: message
        """
        print(message)
        ws.close()

    def listen_for(self, request_data: json, exchange: Exchange) -> ResponseStatus:
        """
        When a request is made to the exchange that requires validation, we start a websocket listener to ensure it is
        successful.
        """
        try:
            self.__key = exchange.key
            self.__secret = exchange.secret
            ws = websocket.WebSocketApp(exchange.websocket, on_open=self.on_open, on_message=self.on_message)
            self.__status = Status.RUNNING
            ws.run_forever()
            print(f"Confirmation from {exchange.name.value} is {ResponseStatus.SUCCESSFUL.value}.")
            self.__status = Status.IDLE
            return ResponseStatus.SUCCESSFUL

        except Exception as e:
            Log.e(e)
            Log.e(f"Confirmation from {exchange.name.value} is {ResponseStatus.UNSUCCESSFUL.value}.")
            return ResponseStatus.UNSUCCESSFUL
