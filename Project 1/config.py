import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Exchange configurations
EXCHANGES = {
    'binance': {
        'api_key': os.getenv('BINANCE_API_KEY', ''),
        'secret': os.getenv('BINANCE_SECRET', ''),
        'sandbox': True  # Set to False for live trading
    },
    'mexc': {
        'api_key': os.getenv('MEXC_API_KEY', ''),
        'secret': os.getenv('MEXC_SECRET', ''),
        'sandbox': True  # Set to False for live trading
    }
}

# Trading parameters
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1h'
LIMIT = 500  # Number of candles to fetch

# Technical indicators parameters
SMA_PERIODS = [20, 50]  # Short and long SMA periods
EMA_PERIODS = [12, 26]  # Short and long EMA periods

# Signal parameters
SIGNAL_THRESHOLD = 0.001  # Minimum price change for signal generation

# Chart parameters
CHART_SAVE_PATH = 'charts'
CHART_FILENAME = 'btc_trading_chart.png' 