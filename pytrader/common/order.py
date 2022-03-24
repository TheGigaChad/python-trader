from pytrader.common.requests import RequestType, RequestStatus
from pytrader.common.asset import Asset


class Order:
    """
    contains the data that gets passed to the request call.
    """
    def __init__(self, request_type: RequestType, asset: Asset):
        self.__type: RequestType = request_type
        self.__asset: Asset = asset
        self.__status: RequestStatus = RequestStatus.INIT

    @property
    def status(self) -> RequestStatus:
        return self.__status

    @status.setter
    def status(self, new_status: RequestStatus):
        self.__status = new_status

    @property
    def type(self) -> RequestType:
        return self.__type

    @property
    def asset(self) -> Asset:
        return self.__asset
