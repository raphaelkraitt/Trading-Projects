import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API Configuration
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# Reddit API Configuration
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = 'CryptoSentimentBot/1.0'

# Trading Configuration
SENTIMENT_THRESHOLD_BUY = 0.3
SENTIMENT_THRESHOLD_SELL = -0.3
SIGNAL_COOLDOWN_HOURS = 1

# Data Collection Settings
MAX_TWEETS_PER_QUERY = 100
MAX_REDDIT_POSTS_PER_QUERY = 50
QUERY_KEYWORDS = ['bitcoin', 'btc', 'crypto', 'cryptocurrency']

# Model Configuration
SENTIMENT_MODEL = 'cardiffnlp/twitter-roberta-base-sentiment-latest'
MAX_TEXT_LENGTH = 512

# Visualization Settings
CHART_SAVE_PATH = 'sentiment_charts'
CHART_FORMAT = 'png' 