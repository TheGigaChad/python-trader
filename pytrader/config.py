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
# # sql
# SQL_SERVER_HOST = os.environ.get("SQL_SERVER_HOST")
# SQL_SERVER_DATABASE = os.environ.get("SQL_SERVER_DATABASE")
# SQL_SERVER_USER = os.environ.get("SQL_SERVER_USER")
# SQL_SERVER_PASSWORD = os.environ.get("SQL_SERVER_PASSWORD")
# SQL_SERVER_WINDOWS_TABLE = os.environ.get("SQL_SERVER_WINDOWS_TABLE")

# TODO - move to .env file
# --------------
# Exchanges Info
# --------------
ALPACA_PAPER_KEY = "PKQWAWCMVV6DD66U9S7D"
ALPACA_PAPER_SECRET = "ObqIv4clTHjt5uGqwVD4CJdGRH3ggQfTef7fOeUa"
ALPACA_PAPER_ADDRESS = "https://paper-api.alpaca.markets"
ALPACA_PAPER_ACCOUNT_NUMBER = "PA3Y2VIN22VU"
ALPACA_PAPER_WEBSOCKET = "wss://paper-api.alpaca.markets/stream"

# --------
# sql Info
# --------
SQL_SERVER_HOST = "156.67.72.201"
SQL_SERVER_DATABASE = "u238726529_stock_trader"
SQL_SERVER_USER = "u238726529_mike"
SQL_SERVER_PASSWORD = "MassiveLegend69"

SQL_SERVER_TRADES_TABLE: str = "algo_trade_trades"
SQL_SERVER_TRADES_TABLE_COLUMN_NAME: str = "`name`"
SQL_SERVER_TRADES_TABLE_COLUMN_ORDER_TYPE: str = "`order_type`"
SQL_SERVER_TRADES_TABLE_COLUMN_QUANTITY: str = "`quantity`"
SQL_SERVER_TRADES_TABLE_COLUMN_ORDER_ID: str = "`order_id`"
SQL_SERVER_TRADES_TABLE_COLUMN_TIMESTAMP: str = "`timestamp`"
SQL_SERVER_TRADES_TABLE_COLUMN_ASSET_TYPE: str = "`asset_type`"

SQL_SERVER_OPEN_TRADES_TABLE: str = "algo_trade_open_trades"
SQL_SERVER_OPEN_TRADES_COLUMN_NAME: str = "`name`"
SQL_SERVER_OPEN_TRADES_COLUMN_ASSET_TYPE: str = "`asset_type`"
SQL_SERVER_OPEN_TRADES_COLUMN_ORDER_TYPE: str = "`order_type`"
SQL_SERVER_OPEN_TRADES_COLUMN_TRADE_INTENT: str = "`trade_intent`"
SQL_SERVER_OPEN_TRADES_COLUMN_QUANTITY: str = "`quantity`"
SQL_SERVER_OPEN_TRADES_COLUMN_ORDER_ID: str = "`trade_id`"
SQL_SERVER_OPEN_TRADES_COLUMN_LAST_UPDATED: str = "`last_updated`"

SQL_SERVER_BUY_SELL_THRESHOLDS_TABLE: str = "`algo_trade_buy_sell_thresholds`"
SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_NAME: str = "`name`"
SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_BUY: str = "`buy`"
SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_SELL: str = "`sell`"
SQL_SERVER_BUY_SELL_THRESHOLDS_COLUMN_LAST_UPDATED: str = "`last_updated`"

SQL_SERVER_WINDOWS_TABLE = "algo_trade_intent_windows"
SQL_SERVER_WINDOWS_COLUMN_NAME = "`name`"
SQL_SERVER_WINDOWS_COLUMN_SMA_SHORT_TRADE = "`sma_short_trade`"
SQL_SERVER_WINDOWS_COLUMN_SMA_LONG_TRADE = "`sma_long_trade`"
SQL_SERVER_WINDOWS_COLUMN_SMA_LONG_HOLD = "`sma_long_hold`"
SQL_SERVER_WINDOWS_COLUMN_EMA_SHORT_TRADE = "`ema_short_trade`"
SQL_SERVER_WINDOWS_COLUMN_EMA_LONG_TRADE = "`ema_long_trade`"
SQL_SERVER_WINDOWS_COLUMN_EMA_LONG_HOLD = "`ema_long_hold`"
SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_SHORT_TRADE = "`macd_fast_short_trade`"
SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_SHORT_TRADE = "`macd_slow_short_trade`"
SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_SHORT_TRADE = "`macd_sig_short_trade`"
SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_LONG_TRADE = "`macd_fast_long_trade`"
SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_LONG_TRADE = "`macd_slow_long_trade`"
SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_LONG_TRADE = "`macd_sig_long_trade`"
SQL_SERVER_WINDOWS_COLUMN_MACD_FAST_LONG_HOLD = "`macd_fast_long_hold`"
SQL_SERVER_WINDOWS_COLUMN_MACD_SLOW_LONG_HOLD = "`macd_slow_long_hold`"
SQL_SERVER_WINDOWS_COLUMN_MACD_SIG_LONG_HOLD = "`macd_sig_long_hold`"
SQL_SERVER_WINDOWS_COLUMN_RSI_SHORT_TRADE = "`rsi_short_trade`"
SQL_SERVER_WINDOWS_COLUMN_RSI_LONG_TRADE = "`rsi_long_trade`"
SQL_SERVER_WINDOWS_COLUMN_RSI_LONG_HOLD = "`rsi_long_hold`"
SQL_SERVER_WINDOWS_COLUMN_VOL_SHORT_TRADE = "`vol_short_trade`"
SQL_SERVER_WINDOWS_COLUMN_VOL_LONG_TRADE = "`vol_long_trade`"
SQL_SERVER_WINDOWS_COLUMN_VOL_LONG_HOLD = "`vol_long_hold`"
SQL_SERVER_WINDOWS_COLUMN_BOLB_SHORT_TRADE = "`bolb_short_trade`"
SQL_SERVER_WINDOWS_COLUMN_BOLB_LONG_TRADE = "`bolb_long_trade`"
SQL_SERVER_WINDOWS_COLUMN_BOLB_LONG_HOLD = "`bolb_long_hold`"

# -----------
# Model repos
# -----------
MODEL_REPO_URL = ""

# ---------------
# User set params
# ---------------
USER_RISK_PARITY_RATIO = 0.6
USER_LONG_TERM_TRADE_RATIO = 0.3
USER_SHORT_TERM_TRADE_RATIO = 0.1
USER_PAPER_MODE = True
USER_USE_RISK_PARITY = False
USER_USE_TRADER = True

USER_OPEN_TRADE_TIME_DELTA = 3600

# --------------------
# Developer set params
# --------------------
DEV_TEST_MODE = True
