import os
from dotenv import load_dotenv

load_dotenv()

# MT5 Connection
MT5_LOGIN = os.getenv('MT5_LOGIN')  # Optional, for real accounts
MT5_PASSWORD = os.getenv('MT5_PASSWORD')  # Optional
MT5_SERVER = os.getenv('MT5_SERVER')  # Optional
MT5_PATH = os.getenv('MT5_PATH', None)  # Optional, path to terminal64.exe

# Trading Settings
SYMBOL = 'AAPL'
TIMEFRAME = 'H1'  # Hourly
HIST_BARS = 500

# RSI Settings
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# MACD Settings
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Visualization
CHART_SAVE_PATH = 'charts'
CHART_FORMAT = 'png'

# Simulated Trading
INITIAL_BALANCE = 10000
TRADE_SIZE = 10  # Number of shares per trade 