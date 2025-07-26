import os
from dotenv import load_dotenv

load_dotenv()

# Trading symbols
SYMBOLS = ['BTC/USDT', 'ETH/USDT']
EXCHANGE = 'binance'

# GUI settings
UPDATE_INTERVAL = 5000  # milliseconds
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Portfolio settings
INITIAL_BALANCE = 10000  # USDT
TRADE_SIZE = 0.01  # BTC/ETH per trade

# Visualization
CHART_SAVE_PATH = 'charts'
CHART_FORMAT = 'png' 