import json
from typing import List, Optional

from yarl import URL

from pytrader import common
from pytrader import exchange


class ExchangeStock(exchange.Exchange):
    """
    Extends the Exchange Class, returning correct data for the Paper Stock Exchange. We are using Alpaca.
    """

    def __init__(self):
        super().__init__(exchange.ExchangeName.ALPACA_PAPER, exchange.ExchangeType.PAPER_STOCK)

    def get_url(self) -> URL:
        pass

    def get_key(self) -> str:
        pass

    def get_secret(self) -> str:
        pass

    def get_cash(self) -> float:
        pass

    def get_holdings(self) -> List[common.Asset]:
        pass

    def get_websocket(self) -> str:
        pass

    def determine_allowance(self) -> float:
        pass

    def fulfill(self, order: common.Order) -> common.ResponseStatus:
        pass

    def buy(self, order: common.Order) -> exchange.ExchangeRequestResponse:
        pass

    def buy_type(self) -> str:
        pass

    def sell(self, order: common.Order) -> exchange.ExchangeRequestResponse:
        pass

    def sell_type(self) -> str:
        pass

    def request_allowance(self) -> float:
        pass

    def request_quantity(self, asset: common.Asset) -> float:
        pass

    def get_trade_intent(self, asset: common.Asset) -> common.TradeIntent:
        pass

    def update_order_status(self, order: common.Order) -> common.OrderStatus:
        pass

    def determine_value(self, asset: common.Asset) -> float:
        pass

    def get_stale_requests(self):
        pass

    def request(self, order: common.Order, request_type: common.RequestType, request_params=None):
        super().request(order, request_type, request_params)

    def asset_to_json(self, request_type: Optional[common.RequestType] = common.RequestType.UNDEFINED) -> json:
        super().asset_to_json(request_type)

    def add_asset(self, asset: common.Asset):
        super().add_asset(asset)
