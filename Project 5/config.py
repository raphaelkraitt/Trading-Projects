import os
from dotenv import load_dotenv

load_dotenv()

# Data settings
SYMBOL = 'BTC/USDT'
EXCHANGE = 'binance'
TIMEFRAME = '1h'
HIST_BARS = 2000
DATA_PATH = 'btcusdt_1h.csv'  # Local cache for historical data

# LSTM Model settings
SEQ_LEN = 48  # Number of past hours to use for prediction
BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 0.001
HIDDEN_SIZE = 64
NUM_LAYERS = 2
TRAIN_TEST_SPLIT = 0.8
MODEL_PATH = 'lstm_price_model.pt'

# Visualization
CHART_SAVE_PATH = 'charts'
CHART_FORMAT = 'png' 