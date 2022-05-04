from typing import Optional, List

from pytrader.common.asset import AssetType
from pytrader.exchange.exchangeManager import ExchangeManager
from pytrader.trade.tradingManager import TradingManager
from pytrader.riskParity.riskParityAsset import RiskParityAsset


class RiskParityManager(TradingManager):
    def __init__(self, exchange_manager: ExchangeManager):
        super().__init__(exchange_manager)
        self.__assets: [RiskParityAsset] = None

    @property
    def assets(self) -> [RiskParityAsset]:
        return self.__assets

    def start(self):
        print("rpm started")
        super().start()

    def stop(self):
        pass

    def init(self):
        pass

    def generatePortfolio(self):
        pass

    def updateRisk(self, assets: Optional[RiskParityAsset] = None):
        if assets is not None:
            return assets
        assets=self.__assets

    def get_assets(self, asset_type: Optional[AssetType] = AssetType.UNKNOWN) -> List[RiskParityAsset]:
        pass
        # assets = super().get_assets(asset_type)
        # risk_parity_assets = [RiskParityAsset(asset.name, asset.type) for asset in assets]
        # self.determineRisk(risk_parity_assets)
        # return risk_parity_assets


