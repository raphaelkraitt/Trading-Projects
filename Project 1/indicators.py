import pandas as pd
import numpy as np

def calculate_sma(data, period):
    """
    Calculate Simple Moving Average
    
    Args:
        data (pd.Series): Price data
        period (int): Period for SMA calculation
    
    Returns:
        pd.Series: SMA values
    """
    return data.rolling(window=period).mean()

def calculate_ema(data, period):
    """
    Calculate Exponential Moving Average
    
    Args:
        data (pd.Series): Price data
        period (int): Period for EMA calculation
    
    Returns:
        pd.Series: EMA values
    """
    return data.ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    """
    Calculate Relative Strength Index
    
    Args:
        data (pd.Series): Price data
        period (int): Period for RSI calculation
    
    Returns:
        pd.Series: RSI values
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(data, period=20, std_dev=2):
    """
    Calculate Bollinger Bands
    
    Args:
        data (pd.Series): Price data
        period (int): Period for calculation
        std_dev (float): Standard deviation multiplier
    
    Returns:
        tuple: (upper_band, middle_band, lower_band)
    """
    middle_band = data.rolling(window=period).mean()
    std = data.rolling(window=period).std()
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    return upper_band, middle_band, lower_band

def detect_crossover(series1, series2):
    """
    Detect crossover between two series
    
    Args:
        series1 (pd.Series): First series
        series2 (pd.Series): Second series
    
    Returns:
        pd.Series: 1 for bullish crossover, -1 for bearish crossover, 0 for no crossover
    """
    crossover = pd.Series(0, index=series1.index)
    
    # Bullish crossover (series1 crosses above series2)
    bullish = (series1 > series2) & (series1.shift(1) <= series2.shift(1))
    crossover[bullish] = 1
    
    # Bearish crossover (series1 crosses below series2)
    bearish = (series1 < series2) & (series1.shift(1) >= series2.shift(1))
    crossover[bearish] = -1
    
    return crossover 