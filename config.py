import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# EXCHANGES
ALPACA_PAPER_KEY = os.environ.get("ALPACA_PAPER_KEY")
ALPACA_PAPER_SECRET = os.environ.get("ALPACA_PAPER_SECRET")
ALPACA_PAPER_ADDRESS = os.environ.get("ALPACA_PAPER_ADDRESS")
ALPACA_PAPER_ACCOUNT_NUMBER = os.environ.get("ALPACA_PAPER_ACCOUNT_NUMBER")

# SQL
SQL_SERVER_HOST = os.environ.get("SQL_SERVER_HOST")
SQL_SERVER_DATABASE = os.environ.get("SQL_SERVER_DATABASE")
SQL_SERVER_USER = os.environ.get("SQL_SERVER_USER")
SQL_SERVER_PASSWORD = os.environ.get("SQL_SERVER_PASSWORD")
SQL_SERVER_WINDOWS_TABLE = os.environ.get("SQL_SERVER_WINDOWS_TABLE")
