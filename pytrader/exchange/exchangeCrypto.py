import json
from random import random
from typing import List, Optional

import alpaca_trade_api
from yarl import URL

from pytrader.cfg import config as cfg
from pytrader.common.asset import Asset
from pytrader.common.order import Order
from pytrader.common.requests import ResponseStatus, RequestType
from pytrader.exchange.exchange import Exchange, ExchangeName, ExchangeType, ExchangeRequestResponse


class ExchangeStockPaper(Exchange):
    """
    Extends the Exchange Class, returning correct data for the Paper Stock Exchange. We are using Alpaca.
    """

    def __init__(self):
        super().__init__(ExchangeName.ALPACA_PAPER, ExchangeType.PAPER_STOCK)

    def get_url(self) -> URL:
        pass

    def get_key(self) -> str:
        pass

    def get_secret(self) -> str:
        pass

    def get_cash(self) -> float:
        pass

    def get_holdings(self) -> List[Asset]:
        pass

    def get_websocket(self) -> str:
        pass

    def determine_allowance(self) -> float:
        pass

    def buy(self, order: Order) -> ExchangeRequestResponse:
        pass

    def buy_type(self) -> str:
        pass

    def sell(self, order: Order) -> ExchangeRequestResponse:
        pass

    def sell_type(self) -> str:
        pass

    def request_allowance(self) -> float:
        pass

    def request_quantity(self, asset: Asset) -> float:
        pass

    def ignore_response(self) -> bool:
        pass

    def get_stale_requests(self):
        pass

    def request(self, order: Order, request_type: RequestType, request_params=None):
        super().request(order, request_type, request_params)

    def asset_to_json(self, request_type: Optional[RequestType] = RequestType.UNDEFINED) -> json:
        super().asset_to_json(request_type)

    def add_asset(self, asset: Asset):
        super().add_asset(asset)
