import os
from dotenv import load_dotenv

load_dotenv()

# Arbitrage settings
SYMBOL = 'BTC/USDT'
TRADE_AMOUNT = 0.01  # BTC per trade
BINANCE_FEE = 0.001  # 0.1%
MEXC_FEE = 0.001  # 0.1%
MIN_PROFIT_USDT = 1.0  # Minimum profit to trigger arbitrage

# Simulation
INITIAL_BALANCE = 10000  # USDT

# Visualization
CHART_SAVE_PATH = 'charts'
CHART_FORMAT = 'png' 