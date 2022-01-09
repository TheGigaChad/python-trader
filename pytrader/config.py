import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# # EXCHANGES
# ALPACA_PAPER_KEY = os.environ.get("ALPACA_PAPER_KEY")
# ALPACA_PAPER_SECRET = os.environ.get("ALPACA_PAPER_SECRET")
# ALPACA_PAPER_ADDRESS = os.environ.get("ALPACA_PAPER_ADDRESS")
# ALPACA_PAPER_ACCOUNT_NUMBER = os.environ.get("ALPACA_PAPER_ACCOUNT_NUMBER")
#
# # SQL
# SQL_SERVER_HOST = os.environ.get("SQL_SERVER_HOST")
# SQL_SERVER_DATABASE = os.environ.get("SQL_SERVER_DATABASE")
# SQL_SERVER_USER = os.environ.get("SQL_SERVER_USER")
# SQL_SERVER_PASSWORD = os.environ.get("SQL_SERVER_PASSWORD")
# SQL_SERVER_WINDOWS_TABLE = os.environ.get("SQL_SERVER_WINDOWS_TABLE")

# TODO - move to .env file
# Exchanges Info
ALPACA_PAPER_KEY = "PKQWAWCMVV6DD66U9S7D"
ALPACA_PAPER_SECRET = "ObqIv4clTHjt5uGqwVD4CJdGRH3ggQfTef7fOeUa"
ALPACA_PAPER_ADDRESS = "https://paper-api.alpaca.markets"
ALPACA_PAPER_ACCOUNT_NUMBER = "PA3Y2VIN22VU"
ALPACA_PAPER_WEBSOCKET = "wss://paper-api.alpaca.markets/stream"


# SQL Info
SQL_SERVER_HOST = "156.67.72.201"
SQL_SERVER_DATABASE = "u238726529_stock_trader"
SQL_SERVER_USER = "u238726529_mike"
SQL_SERVER_PASSWORD = "MassiveLegend69"
SQL_SERVER_WINDOWS_TABLE = "algo_trade_intent_windows"

# User set params
USER_RISK_PARITY_RATIO = 0.6
USER_LONG_TERM_TRADE_RATIO = 0.3
USER_SHORT_TERM_TRADE_RATIO = 0.1
USER_PAPER_MODE = True
USER_USE_RISK_PARITY = False
USER_USE_TRADER = True
