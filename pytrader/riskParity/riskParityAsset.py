from pytrader.common.asset import Asset, AssetType


class RiskParityAsset(Asset):
    def __init__(self, name: str, asset_type: AssetType):
        super().__init__(name, asset_type)
        self.__risk = None

    @property
    def risk(self):
        return self.__risk

    @risk.setter
    def risk(self, val):
        self.__risk = val




