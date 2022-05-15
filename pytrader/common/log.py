import logging.config
import os
import traceback
from pathlib import Path

BASE_LOG_FORMAT = '[%(levelname)s] - %(asctime)s - %(name)s : %(message)s'
LOG_DATE_FORMAT = '%m/%d/%Y %I:%M:%S%p'
LOG_FILE_PATH = Path(__file__).parent.parent / 'log.log'


class Log:
    """
    Logging class to make formatting and logging substantially easier.
    """

    def __init__(self, tag: str):
        self.logger = logging.getLogger(os.path.basename(tag))
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(LOG_FILE_PATH)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(BASE_LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def d(self, *args):
        """
        logs a debug level log in console and log file.
        :param args: list of items to be logged, added on a single row with one space inbetween.
        """
        message = " ".join(args)
        self.logger.debug(message)

    def e(self, *args):
        """
        logs an error level log in console and log file.
        :param args: list of items to be logged, added on a single row with one space inbetween.
        """
        message = " ".join(args)
        self.logger.error(message)

    def i(self, *args):
        """
        logs a info level log in console and log file.
        :param args: list of items to be logged, added on a single row with one space inbetween.
        """
        message = " ".join(args)
        self.logger.info(message)

    def c(self, *args):
        """
        logs a critical level log in console and log file.
        :param args: list of items to be logged, added on a single row with one space inbetween.
        """
        message = " ".join(args)
        self.logger.critical(message)

    def w(self, *args):
        """
        logs a warning level log in console and log file.
        :param args: list of items to be logged, added on a single row with one space inbetween.
        """
        message = " ".join(args)
        self.logger.warning(message)

