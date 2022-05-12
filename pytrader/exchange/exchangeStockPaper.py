import json
from random import random
from typing import List, Optional

import alpaca_trade_api
from yarl import URL

from pytrader.cfg import config as cfg
from pytrader.common.asset import Asset, AssetType
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
        return cfg.ALPACA_PAPER_ADDRESS

    def get_key(self) -> str:
        return cfg.ALPACA_PAPER_KEY

    def get_secret(self) -> str:
        return cfg.ALPACA_PAPER_SECRET

    def get_cash(self) -> float:
        api = alpaca_trade_api.REST(self.get_key(), self.get_secret(), self.get_url())
        cash = float(api.get_account().cash)
        api.close()
        return cash

    def get_holdings(self) -> List[Asset]:
        api = alpaca_trade_api.REST(self.get_key(), self.get_secret(), self.get_url())
        assets = api.list_positions()
        api.close()
        holdings: List[Asset] = []
        if assets is not None:
            for asset in assets:
                a: Asset = Asset(asset.symbol, AssetType.PAPER_STOCK)
                a.qty = asset.qty
                a.value = asset.market_value
                a.trade_intent = self.__get_trade_intent(a)
                print(asset)
                holdings.append(a)
        return holdings

    def get_websocket(self) -> str:
        return cfg.ALPACA_PAPER_WEBSOCKET

    def determine_allowance(self) -> float:
        # TODO calc
        return 1.0

    def buy(self, order: Order) -> ExchangeRequestResponse:
        api = alpaca_trade_api.REST(self.get_key(), self.get_secret(), self.get_url())
        qty = self.determine_allowance()
        order_id = "1" + str(random.randrange(1, 10000000))
        api.submit_order(symbol=order.asset.name, qty=qty, side="buy", type=self.buy_type(),
                         client_order_id=order_id)
        api.close()

        return ExchangeRequestResponse(ResponseStatus.SUCCESSFUL, request_params=None,
                                       listen_required=not self.ignore_response())

    def buy_type(self) -> str:
        # TODO calc
        return "market"

    def sell(self, order: Order) -> ExchangeRequestResponse:
        api = alpaca_trade_api.REST(self.get_key(), self.get_secret(), self.get_url())
        qty = api.get_position(symbol=order.asset.name).qty
        order_id = "2" + str(random.randrange(1, 10000000))
        api.submit_order(symbol=order.asset.name, qty=qty, side="sell", type=self.sell_type(),
                         client_order_id=order_id)
        api.close()
        return ExchangeRequestResponse(ResponseStatus.SUCCESSFUL, request_params=None,
                                       listen_required=not self.ignore_response())

    def sell_type(self) -> str:
        return "market"

    def request_allowance(self) -> float:
        # TODO - work
        return 1000.0

    def request_quantity(self, asset: Asset) -> float:
        # TODO - work
        return 1.0

    def ignore_response(self) -> bool:
        is_market_open: bool = alpaca_trade_api.REST(cfg.ALPACA_PAPER_KEY, cfg.ALPACA_PAPER_SECRET,
                                                     cfg.ALPACA_PAPER_ADDRESS).get_clock().is_open
        if (self.__type == ExchangeType.STOCK or self.__type == ExchangeType.PAPER_STOCK) and not is_market_open:
            print("Market closed, ignoring response")
            return True
        else:
            return False

    def get_stale_requests(self):
        pass

    def request(self, order: Order, request_type: RequestType, request_params=None):
        super().request(order, request_type, request_params)

    def asset_to_json(self, request_type: Optional[RequestType] = RequestType.UNDEFINED) -> json:
        super().asset_to_json(request_type)

    def add_asset(self, asset: Asset):
        super().add_asset(asset)