from pathlib import Path

from urllib3.util import Url

from pytrader.common.status import Status
from pytrader.config import MODEL_REPO_URL


class ModelManager:
    """
    Handles the retrieval of the models used by the trade manager subprocesses to determine trade opportunities.
    """
    def __init__(self):
        self.__status: Status = Status.INIT
        self.__repo: Path = Path(__file__).parent / "data"
        self.__url: Url = self.__getURL()

    @property
    def repo(self):
        return self.__repo

    def __getURL(self) -> Url:
        return MODEL_REPO_URL

    def load(self):
        self.__status = Status.STARTING
        # TODO - load models here
        self.__status = Status.RUNNING
