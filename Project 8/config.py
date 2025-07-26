import os
from dotenv import load_dotenv

load_dotenv()

# Data settings
SYMBOL = 'BTC/USDT'
EXCHANGE = 'binance'
TIMEFRAME = '1h'
HIST_BARS = 2000
DATA_PATH = 'btcusdt_1h.csv'  # Local cache for historical data

# Strategy settings
SMA_FAST = 20
SMA_SLOW = 50
TRADE_SIZE = 0.01  # BTC per trade
FEE = 0.001  # 0.1% per trade

# Backtest settings
INITIAL_BALANCE = 10000  # USDT

# Visualization
CHART_SAVE_PATH = 'charts'
CHART_FORMAT = 'png' 