import pandas as pd
import numpy as np
from indicators import calculate_sma, calculate_ema, detect_crossover, calculate_rsi, calculate_bollinger_bands
from config import SMA_PERIODS, EMA_PERIODS, SIGNAL_THRESHOLD

class SignalGenerator:
    def __init__(self):
        self.signals = []
    
    def calculate_indicators(self, df):
        """
        Calculate all technical indicators for the given DataFrame
        
        Args:
            df (pd.DataFrame): OHLCV data
        
        Returns:
            pd.DataFrame: DataFrame with indicators added
        """
        # Calculate SMAs
        for period in SMA_PERIODS:
            df[f'sma_{period}'] = calculate_sma(df['close'], period)
        
        # Calculate EMAs
        for period in EMA_PERIODS:
            df[f'ema_{period}'] = calculate_ema(df['close'], period)
        
        # Calculate RSI
        df['rsi'] = calculate_rsi(df['close'])
        
        # Calculate Bollinger Bands
        bb_upper, bb_middle, bb_lower = calculate_bollinger_bands(df['close'])
        df['bb_upper'] = bb_upper
        df['bb_middle'] = bb_middle
        df['bb_lower'] = bb_lower
        
        return df
    
    def generate_signals(self, df):
        """
        Generate buy/sell signals based on technical indicators
        
        Args:
            df (pd.DataFrame): DataFrame with indicators
        
        Returns:
            pd.DataFrame: DataFrame with signals added
        """
        # Initialize signal columns
        df['sma_signal'] = 0
        df['ema_signal'] = 0
        df['rsi_signal'] = 0
        df['bb_signal'] = 0
        df['combined_signal'] = 0
        
        # SMA crossover signals
        if len(SMA_PERIODS) >= 2:
            short_sma = f'sma_{SMA_PERIODS[0]}'
            long_sma = f'sma_{SMA_PERIODS[1]}'
            df['sma_signal'] = detect_crossover(df[short_sma], df[long_sma])
        
        # EMA crossover signals
        if len(EMA_PERIODS) >= 2:
            short_ema = f'ema_{EMA_PERIODS[0]}'
            long_ema = f'ema_{EMA_PERIODS[1]}'
            df['ema_signal'] = detect_crossover(df[short_ema], df[long_ema])
        
        # RSI signals
        df.loc[df['rsi'] < 30, 'rsi_signal'] = 1  # Oversold - buy signal
        df.loc[df['rsi'] > 70, 'rsi_signal'] = -1  # Overbought - sell signal
        
        # Bollinger Bands signals
        df.loc[df['close'] <= df['bb_lower'], 'bb_signal'] = 1  # Price at lower band - buy signal
        df.loc[df['close'] >= df['bb_upper'], 'bb_signal'] = -1  # Price at upper band - sell signal
        
        # Combined signal (simple average of all signals)
        signal_columns = ['sma_signal', 'ema_signal', 'rsi_signal', 'bb_signal']
        df['combined_signal'] = df[signal_columns].mean(axis=1)
        
        # Apply threshold to combined signal
        df.loc[df['combined_signal'] >= SIGNAL_THRESHOLD, 'final_signal'] = 1  # Buy
        df.loc[df['combined_signal'] <= -SIGNAL_THRESHOLD, 'final_signal'] = -1  # Sell
        df.loc[(df['combined_signal'] > -SIGNAL_THRESHOLD) & (df['combined_signal'] < SIGNAL_THRESHOLD), 'final_signal'] = 0  # Hold
        
        return df
    
    def get_latest_signals(self, df):
        """
        Get the latest signals from the DataFrame
        
        Args:
            df (pd.DataFrame): DataFrame with signals
        
        Returns:
            dict: Latest signals and recommendations
        """
        latest = df.iloc[-1]
        
        signals = {
            'timestamp': latest.name,
            'price': latest['close'],
            'sma_signal': latest['sma_signal'],
            'ema_signal': latest['ema_signal'],
            'rsi_signal': latest['rsi_signal'],
            'bb_signal': latest['bb_signal'],
            'combined_signal': latest['combined_signal'],
            'final_signal': latest['final_signal'],
            'recommendation': self._get_recommendation(latest['final_signal'])
        }
        
        return signals
    
    def _get_recommendation(self, signal):
        """
        Convert signal to recommendation
        
        Args:
            signal (float): Signal value
        
        Returns:
            str: Recommendation
        """
        if signal == 1:
            return "BUY"
        elif signal == -1:
            return "SELL"
        else:
            return "HOLD"
    
    def get_signal_summary(self, df):
        """
        Get a summary of all signals in the DataFrame
        
        Args:
            df (pd.DataFrame): DataFrame with signals
        
        Returns:
            dict: Signal summary
        """
        buy_signals = len(df[df['final_signal'] == 1])
        sell_signals = len(df[df['final_signal'] == -1])
        hold_signals = len(df[df['final_signal'] == 0])
        
        total_signals = buy_signals + sell_signals + hold_signals
        
        return {
            'total_periods': total_signals,
            'buy_signals': buy_signals,
            'sell_signals': sell_signals,
            'hold_signals': hold_signals,
            'buy_percentage': (buy_signals / total_signals * 100) if total_signals > 0 else 0,
            'sell_percentage': (sell_signals / total_signals * 100) if total_signals > 0 else 0,
            'hold_percentage': (hold_signals / total_signals * 100) if total_signals > 0 else 0
        } 