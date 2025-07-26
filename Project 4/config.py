import os
from dotenv import load_dotenv

load_dotenv()

# Data settings
SYMBOL = 'ETH/USDT'
EXCHANGE = 'binance'
TIMEFRAME = '1h'
HIST_BARS = 2000
DATA_PATH = 'ethusdt_1h.csv'  # Local cache for historical data

# RL Environment settings
INITIAL_BALANCE = 10000
TRANSACTION_FEE = 0.001  # 0.1% per trade
MAX_POSITION = 1  # Max 1 ETH long or short
WINDOW_SIZE = 48  # Number of bars in observation window

# Training settings
TOTAL_TIMESTEPS = 100_000
EVAL_EPISODES = 10
MODEL_PATH = 'rl_trading_model.zip'

# Visualization
CHART_SAVE_PATH = 'charts'
CHART_FORMAT = 'png' 