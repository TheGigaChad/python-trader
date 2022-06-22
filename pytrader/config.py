import os

from alpaca_trade_api.common import URL
from dotenv import load_dotenv

load_dotenv()

# --------------
# Exchanges Info
# --------------
ALPACA_PAPER_KEY: str = os.environ.get("ALPACA_PAPER_KEY")
ALPACA_PAPER_SECRET: str = os.environ.get("ALPACA_PAPER_SECRET")
ALPACA_PAPER_ADDRESS: URL = URL(os.environ.get("ALPACA_PAPER_ADDRESS"))
ALPACA_PAPER_ACCOUNT_NUMBER: str = os.environ.get("ALPACA_PAPER_ACCOUNT_NUMBER")
ALPACA_PAPER_WEBSOCKET: str = os.environ.get("ALPACA_PAPER_WEBSOCKET")

# --------
# sql Info
# --------
SQL_SERVER_HOST: str = os.environ.get("SQL_SERVER_HOST")
SQL_SERVER_DATABASE: str = os.environ.get("SQL_SERVER_DATABASE")
SQL_SERVER_USER: str = os.environ.get("SQL_SERVER_USER")
SQL_SERVER_PASSWORD: str = os.environ.get("SQL_SERVER_PASSWORD")

SQL_SERVER_TRADES_TABLE: str = os.environ.get("SQL_SERVER_TRADES_TABLE")
SQL_SERVER_TRADES_TABLE_COLUMN_NAME: str = os.environ.get("SQL_SERVER_TRADES_TABLE_COLUMN_NAME")
SQL_SERVER_TRADES_TABLE_COLUMN_ORDER_TYPE: str = os.environ.get("SQL_SERVER_TRADES_TABLE_COLUMN_ORDER_TYPE")
SQL_SERVER_TRADES_TABLE_COLUMN_QUANTITY: str = os.environ.get("SQL_SERVER_TRADES_TABLE_COLUMN_QUANTITY")
SQL_SERVER_TRADES_TABLE_COLUMN_ORDER_ID: str = os.environ.get("SQL_SERVER_TRADES_TABLE_COLUMN_ORDER_ID")
SQL_SERVER_TRADES_TABLE_COLUMN_TIMESTAMP: str = os.environ.get("SQL_SERVER_TRADES_TABLE_COLUMN_TIMESTAMP")
SQL_SERVER_TRADES_TABLE_COLUMN_ASSET_TYPE: str = os.environ.get("SQL_SERVER_TRADES_TABLE_COLUMN_ASSET_TYPE")

SQL_SERVER_OPEN_TRADES_TABLE: str = os.environ.get("SQL_SERVER_OPEN_TRADES_TABLE")
SQL_SERVER_OPEN_TRADES_COLUMN_NAME: str = os.environ.get("SQL_SERVER_OPEN_TRADES_COLUMN_NAME")
SQL_SERVER_OPEN_TRADES_COLUMN_ASSET_TYPE: str = os.environ.get("SQL_SERVER_OPEN_TRADES_COLUMN_ASSET_TYPE")
SQL_SERVER_OPEN_TRADES_COLUMN_ORDER_TYPE: str = os.environ.get("SQL_SERVER_OPEN_TRADES_COLUMN_ORDER_TYPE")
SQL_SERVER_OPEN_TRADES_COLUMN_TRADE_INTENT: str = os.environ.get("SQL_SERVER_OPEN_TRADES_COLUMN_TRADE_INTENT")
SQL_SERVER_OPEN_TRADES_COLUMN_QUANTITY: str = os.environ.get("SQL_SERVER_OPEN_TRADES_COLUMN_QUANTITY")
SQL_SERVER_OPEN_TRADES_COLUMN_ORDER_ID: str = os.environ.get("SQL_SERVER_OPEN_TRADES_COLUMN_ORDER_ID")
SQL_SERVER_OPEN_TRADES_COLUMN_LAST_UPDATED: str = os.environ.get("SQL_SERVER_OPEN_TRADES_COLUMN_LAST_UPDATED")

SQL_SERVER_BUY_SELL_THRESHOLDS_TABLE: str = os.environ.get("SQL_SERVER_BUY_SELL_THRESHOLDS_TABLE")
SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_NAME: str = os.environ.get("SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_NAME")
SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_BUY: str = os.environ.get("SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_BUY")
SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_SELL: str = os.environ.get("SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_SELL")
SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_LAST_UPDATED: str = os.environ.get(
    "SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_LAST_UPDATED")

SQL_SERVER_WINDOWS_TABLE: str = os.environ.get("SQL_SERVER_WINDOWS_TABLE")
SQL_SERVER_WINDOWS_COLUMN_NAME: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_NAME")
SQL_SERVER_WINDOWS_COLUMN_SMA_SHORT_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_SMA_SHORT_TRADE")
SQL_SERVER_WINDOWS_COLUMN_SMA_LONG_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_SMA_LONG_TRADE")
SQL_SERVER_WINDOWS_COLUMN_SMA_LONG_HOLD: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_SMA_LONG_HOLD")
SQL_SERVER_WINDOWS_COLUMN_EMA_SHORT_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_EMA_SHORT_TRADE")
SQL_SERVER_WINDOWS_COLUMN_EMA_LONG_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_EMA_LONG_TRADE")
SQL_SERVER_WINDOWS_COLUMN_EMA_LONG_HOLD: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_EMA_LONG_HOLD")
SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_SHORT_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_SHORT_TRADE")
SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_SHORT_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_SHORT_TRADE")
SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_SHORT_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_SHORT_TRADE")
SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_LONG_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_LONG_TRADE")
SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_LONG_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_LONG_TRADE")
SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_LONG_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_LONG_TRADE")
SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_LONG_HOLD: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_LONG_HOLD")
SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_LONG_HOLD: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_LONG_HOLD")
SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_LONG_HOLD: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_LONG_HOLD")
SQL_SERVER_WINDOWS_COLUMN_RSI_SHORT_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_RSI_SHORT_TRADE")
SQL_SERVER_WINDOWS_COLUMN_RSI_LONG_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_RSI_LONG_TRADE")
SQL_SERVER_WINDOWS_COLUMN_RSI_LONG_HOLD: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_RSI_LONG_HOLD")
SQL_SERVER_WINDOWS_COLUMN_VOL_SHORT_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_VOL_SHORT_TRADE")
SQL_SERVER_WINDOWS_COLUMN_VOL_LONG_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_VOL_LONG_TRADE")
SQL_SERVER_WINDOWS_COLUMN_VOL_LONG_HOLD: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_VOL_LONG_HOLD")
SQL_SERVER_WINDOWS_COLUMN_BOLB_SHORT_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_BOLB_SHORT_TRADE")
SQL_SERVER_WINDOWS_COLUMN_BOLB_LONG_TRADE: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_BOLB_LONG_TRADE")
SQL_SERVER_WINDOWS_COLUMN_BOLB_LONG_HOLD: str = os.environ.get("SQL_SERVER_WINDOWS_COLUMN_BOLB_LONG_HOLD")

# --------
# aws Info
# --------
AWS_IAM_USERNAME: str = os.environ.get("AWS_IAM_USERNAME")
AWS_IAM_PASSWORD: str = os.environ.get("AWS_IAM_PASSWORD")
AWS_IAM_KEY: str = os.environ.get("AWS_IAM_KEY")
AWS_IAM_SECRET: str = os.environ.get("AWS_IAM_SECRET")
AWS_IAM_CONSOLE_LOGIN_LINK: str = os.environ.get("AWS_IAM_CONSOLE_LOGIN_LINK")
AWS_MODEL_BUCKET_NAME: str = os.environ.get("AWS_MODEL_BUCKET_NAME")

# -----------
# Model repos
# -----------
MODEL_REPO_URL = ""

# ---------------
# User set params
# ---------------
USER_RISK_PARITY_RATIO: float = 0.6
USER_LONG_TERM_TRADE_RATIO: float = 0.3
USER_SHORT_TERM_TRADE_RATIO: float = 0.1
USER_PAPER_MODE: bool = True
USER_USE_RISK_PARITY: bool = False
USER_USE_TRADER: bool = True
USER_OPEN_TRADE_TIME_DELTA: int = 3600

# --------------------
# Developer set params
# --------------------
DEV_TEST_MODE: bool = True
