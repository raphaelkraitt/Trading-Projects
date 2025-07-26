import os
from dotenv import load_dotenv

load_dotenv()

# MT5 Connection
MT5_LOGIN = os.getenv('MT5_LOGIN')  # Optional
MT5_PASSWORD = os.getenv('MT5_PASSWORD')  # Optional
MT5_SERVER = os.getenv('MT5_SERVER')  # Optional
MT5_PATH = os.getenv('MT5_PATH', None)  # Optional

# Portfolio settings
PORTFOLIO_SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
TARGET_WEIGHTS = [0.2, 0.2, 0.2, 0.2, 0.2]  # Equal weight by default

# Optimization
RISK_FREE_RATE = 0.01  # 1% annual
HIST_BARS = 252  # 1 year of daily data

# Visualization
CHART_SAVE_PATH = 'charts'
CHART_FORMAT = 'png' 