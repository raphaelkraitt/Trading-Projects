import os
from dotenv import load_dotenv

load_dotenv()

# MT5 Connection
MT5_LOGIN = os.getenv('MT5_LOGIN')  # Optional
MT5_PASSWORD = os.getenv('MT5_PASSWORD')  # Optional
MT5_SERVER = os.getenv('MT5_SERVER')  # Optional
MT5_PATH = os.getenv('MT5_PATH', None)  # Optional

# News API settings
NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'demo')  # Use 'demo' for testing
NEWS_SYMBOL = 'TSLA'
NEWS_QUERY = 'Tesla'
MAX_ARTICLES = 20

# Sentiment settings
SENTIMENT_THRESHOLD_BUY = 0.1
SENTIMENT_THRESHOLD_SELL = -0.1
SIGNAL_COOLDOWN_HOURS = 1

# Trading settings
SYMBOL = 'TSLA'
TRADE_SIZE = 10  # Number of shares per trade

# Visualization
CHART_SAVE_PATH = 'charts'
CHART_FORMAT = 'png' 