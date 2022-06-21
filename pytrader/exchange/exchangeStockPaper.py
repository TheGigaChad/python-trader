import json
from typing import List, Optional

import alpaca_trade_api
from yarl import URL

from pytrader import common, exchange
from pytrader.cfg import config as cfg

Log = common.Log(__file__)


class ExchangeStockPaper(exchange.Exchange):
    """
    Extends the Exchange Class, returning correct data for the Paper Stock Exchange. We are using Alpaca.
    """

    def __init__(self):
        super().__init__(exchange.ExchangeName.ALPACA_PAPER, exchange.ExchangeType.PAPER_STOCK)

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

    def get_holdings(self) -> List[common.Asset]:
        api = alpaca_trade_api.REST(self.get_key(), self.get_secret(), self.get_url())
        assets = api.list_positions()
        api.close()
        holdings: List[common.Asset] = []
        if assets is not None:
            for asset in assets:
                a: common.Asset = common.Asset(asset.symbol, common.AssetType.PAPER_STOCK)
                a.qty = asset.qty
                a.value = asset.market_value
                a.trade_intent = self.get_trade_intent(a)
                holdings.append(a)
        return holdings

    def get_websocket(self) -> str:
        return cfg.ALPACA_PAPER_WEBSOCKET

    def determine_allowance(self) -> float:
        # TODO calc
        return 1.0

    def fulfill(self, order: common.Order) -> exchange.ExchangeRequestResponse:
        if order.type == common.OrderType.BUY:
            return self.buy(order)
        elif order.type == common.OrderType.SELL:
            return self.sell(order)

    def buy(self, order: common.Order) -> exchange.ExchangeRequestResponse:
        api = alpaca_trade_api.REST(self.get_key(), self.get_secret(), self.get_url())
        qty = self.determine_allowance()
        api.submit_order(symbol=order.asset.name, qty=qty, side="buy", type=self.buy_type(),
                         client_order_id=str(order.asset.id))
        api.close()
        Log.i(f"Successfully bought {qty} {order.asset.name}")
        return exchange.ExchangeRequestResponse(common.ResponseStatus.SUCCESSFUL, request_params=None,
                                                listen_required=False)

    def buy_type(self) -> str:
        # TODO calc
        return "market"

    def sell(self, order: common.Order) -> exchange.ExchangeRequestResponse:
        api = alpaca_trade_api.REST(self.get_key(), self.get_secret(), self.get_url())
        qty = api.get_position(symbol=order.asset.name).qty
        api.submit_order(symbol=order.asset.name, qty=qty, side="sell", type=self.sell_type(),
                         client_order_id=str(order.asset.id))
        api.close()
        Log.i(f"Successfully sold {qty} {order.asset.name}")
        return exchange.ExchangeRequestResponse(common.ResponseStatus.SUCCESSFUL, request_params=None,
                                                listen_required=False)

    def sell_type(self) -> str:
        return "market"

    def request_allowance(self) -> float:
        # TODO - work
        return 1000.0

    def request_quantity(self, asset: common.Asset) -> float:
        # TODO - work
        return 1.0

    def get_trade_intent(self, asset: common.Asset) -> common.TradeIntent:
        # TODO - work
        return common.TradeIntent.SHORT_TRADE

    def update_order_status(self, order: common.Order) -> common.Order:
        api = alpaca_trade_api.REST(self.get_key(), self.get_secret(), self.get_url())
        list_orders = api.list_orders()
        api.close()
        for list_order in list_orders:
            if list_order.client_order_id != order.asset.id.__str__():
                continue
            if list_order.status == common.OrderStatus.FILLED.value:
                order.status = common.OrderStatus.FILLED
            elif list_order.status == common.OrderStatus.ACCEPTED.value:
                order.asset.qty = order.asset.qty - float(list_order.filled_qty)
                order.status = common.OrderStatus.PROCESSING
            elif list_order.status == common.OrderStatus.REJECTED.value:
                order.status = common.OrderStatus.REJECTED

        return order

    def determine_value(self, asset: common.Asset) -> float:
        api = alpaca_trade_api.REST(self.get_key(), self.get_secret(), self.get_url())
        value: float = float(api.get_latest_bar(asset.name).c)
        api.close()
        return value

    def get_stale_requests(self):
        pass

    def asset_to_json(self, request_type: Optional[common.RequestType] = common.RequestType.UNDEFINED) -> json:
        super().asset_to_json(request_type)

    def add_asset(self, asset: common.Asset):
        super().add_asset(asset)
