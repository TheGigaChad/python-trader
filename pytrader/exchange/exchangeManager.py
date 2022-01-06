import json
from typing import Optional

from exchange import Exchange, ExchangeName, ExchangeType, ExchangeRequestType, ExchangeRequestResponseType
from pytrader.common.asset import Asset, AssetType


class ExchangeManager:
    # TODO - we might need a thread-lock here
    """
    Handles the exchanges and different types of requests etc.  When an asset_thread wants to do something, it should
    make a request to here.
    """
    def __init__(self):
        self.__paper_stock_exchange  = Exchange(exchange_type=ExchangeType.PAPER_STOCK, name=ExchangeName.ALPACA_PAPER)
        self.__paper_crypto_exchange = Exchange(exchange_type=ExchangeType.PAPER_CRYPTO, name=ExchangeName.ALPACA_PAPER)
        self.__stock_exchange = Exchange(exchange_type=ExchangeType.STOCK, name=ExchangeName.ALPACA_PAPER)
        self.__crypto_exchange = Exchange(exchange_type=ExchangeType.CRYPTO, name=ExchangeName.ALPACA_PAPER)

    def request(self, asset: Asset, request_type: ExchangeRequestType, request_params: Optional[json] = None) \
            -> ExchangeRequestResponseType:
        """
        exchange request
        """
        if asset.type == AssetType.PAPER_STOCK:
            return self.__paper_stock_exchange.request(request_type, request_params)
        elif asset.type == AssetType.PAPER_CRYPTO:
            return self.__paper_stock_exchange.request(request_type, request_params)

    def update(self):
        """
        Call to update data on all exchanges.
        """
        self.__paper_stock_exchange.request(ExchangeRequestType.UPDATE)
        self.__paper_crypto_exchange.request(ExchangeRequestType.UPDATE)

    def getAssets(self, asset_type: Optional[AssetType] = AssetType.UNKNOWN) -> list[Asset]:
        """
        determines the assets held based on the asset type.  This will return all assets if you don't specify.
        :param asset_type: type of asset you want specifically.
        :return: all assets owned.
        """
        assets = None
        if asset_type == AssetType.UNKNOWN:
            paper_stock = self.__paper_stock_exchange.holdings
            paper_crypto = self.__paper_crypto_exchange.holdings
            stock = self.__stock_exchange.holdings
            crypto = self.__crypto_exchange.holdings
            assets = paper_stock
            assets.extend(paper_crypto)
            assets.extend(stock)
            assets.extend(crypto)
        elif asset_type == AssetType.PAPER_STOCK:
            assets = self.__paper_stock_exchange.holdings
        elif asset_type == AssetType.PAPER_CRYPTO:
            assets = self.__paper_crypto_exchange.holdings
        elif asset_type == AssetType.STOCK:
            assets = self.__stock_exchange.holdings
        elif asset_type == AssetType.CRYPTO:
            assets = self.__crypto_exchange.holdings
        return assets


