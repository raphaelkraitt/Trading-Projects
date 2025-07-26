import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import os
from datetime import datetime
from config import CHART_SAVE_PATH, CHART_FILENAME

class ChartGenerator:
    def __init__(self):
        self.setup_style()
        self.ensure_chart_directory()
    
    def setup_style(self):
        """Setup matplotlib style for better-looking charts"""
        plt.style.use('dark_background')
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
    
    def ensure_chart_directory(self):
        """Ensure the chart directory exists"""
        if not os.path.exists(CHART_SAVE_PATH):
            os.makedirs(CHART_SAVE_PATH)
            print(f"Created chart directory: {CHART_SAVE_PATH}")
    
    def create_candlestick_chart(self, df, exchange_name, save_path=None):
        """
        Create a comprehensive candlestick chart with indicators
        
        Args:
            df (pd.DataFrame): DataFrame with OHLCV and indicator data
            exchange_name (str): Name of the exchange
            save_path (str): Path to save the chart (optional)
        
        Returns:
            str: Path to saved chart
        """
        # Create figure with subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12), 
                                           gridspec_kw={'height_ratios': [3, 1, 1]})
        
        # Filter data to remove NaN values for better visualization
        plot_df = df.dropna()
        
        if len(plot_df) == 0:
            print("No data to plot after removing NaN values")
            return None
        
        # Plot 1: Candlestick chart with moving averages
        self._plot_candlesticks(ax1, plot_df)
        self._plot_moving_averages(ax1, plot_df)
        self._plot_bollinger_bands(ax1, plot_df)
        self._plot_signals(ax1, plot_df)
        
        ax1.set_title(f'{exchange_name.upper()} - BTC/USDT 1H Chart with Technical Indicators', 
                     fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price (USDT)', fontsize=12)
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: RSI
        self._plot_rsi(ax2, plot_df)
        ax2.set_ylabel('RSI', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Volume
        self._plot_volume(ax3, plot_df)
        ax3.set_ylabel('Volume', fontsize=12)
        ax3.set_xlabel('Date', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        # Format x-axis
        for ax in [ax1, ax2, ax3]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save chart
        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(CHART_SAVE_PATH, f'{exchange_name}_{timestamp}_{CHART_FILENAME}')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        
        print(f"Chart saved: {save_path}")
        return save_path
    
    def _plot_candlesticks(self, ax, df):
        """Plot candlestick chart"""
        # Define colors for candlesticks
        colors = ['green' if close >= open else 'red' 
                 for close, open in zip(df['close'], df['open'])]
        
        # Plot candlesticks
        width = 0.6
        width2 = width * 0.8
        
        # High-low lines
        ax.vlines(df.index, df['low'], df['high'], color=colors, linewidth=1)
        
        # Open-close rectangles
        ax.vlines(df.index, df['open'], df['close'], color=colors, linewidth=width*10)
        
        # Add wicks
        ax.vlines(df.index, df['low'], df['high'], color=colors, linewidth=1)
    
    def _plot_moving_averages(self, ax, df):
        """Plot moving averages"""
        # Plot SMAs
        for period in [20, 50]:
            if f'sma_{period}' in df.columns:
                ax.plot(df.index, df[f'sma_{period}'], 
                       label=f'SMA {period}', linewidth=1.5, alpha=0.8)
        
        # Plot EMAs
        for period in [12, 26]:
            if f'ema_{period}' in df.columns:
                ax.plot(df.index, df[f'ema_{period}'], 
                       label=f'EMA {period}', linewidth=1.5, alpha=0.8)
    
    def _plot_bollinger_bands(self, ax, df):
        """Plot Bollinger Bands"""
        if 'bb_upper' in df.columns and 'bb_lower' in df.columns:
            ax.plot(df.index, df['bb_upper'], label='BB Upper', 
                   color='gray', linewidth=1, alpha=0.7, linestyle='--')
            ax.plot(df.index, df['bb_lower'], label='BB Lower', 
                   color='gray', linewidth=1, alpha=0.7, linestyle='--')
            
            # Fill Bollinger Bands
            ax.fill_between(df.index, df['bb_upper'], df['bb_lower'], 
                           alpha=0.1, color='gray')
    
    def _plot_signals(self, ax, df):
        """Plot buy/sell signals"""
        if 'final_signal' in df.columns:
            # Buy signals
            buy_signals = df[df['final_signal'] == 1]
            if len(buy_signals) > 0:
                ax.scatter(buy_signals.index, buy_signals['low'] * 0.995, 
                          marker='^', color='green', s=100, label='Buy Signal', zorder=5)
            
            # Sell signals
            sell_signals = df[df['final_signal'] == -1]
            if len(sell_signals) > 0:
                ax.scatter(sell_signals.index, sell_signals['high'] * 1.005, 
                          marker='v', color='red', s=100, label='Sell Signal', zorder=5)
    
    def _plot_rsi(self, ax, df):
        """Plot RSI indicator"""
        if 'rsi' in df.columns:
            ax.plot(df.index, df['rsi'], color='purple', linewidth=1.5)
            
            # Add overbought/oversold lines
            ax.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Overbought')
            ax.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Oversold')
            ax.axhline(y=50, color='white', linestyle='-', alpha=0.5)
            
            ax.set_ylim(0, 100)
            ax.legend(loc='upper right')
    
    def _plot_volume(self, ax, df):
        """Plot volume bars"""
        colors = ['green' if close >= open else 'red' 
                 for close, open in zip(df['close'], df['open'])]
        
        ax.bar(df.index, df['volume'], color=colors, alpha=0.7, width=0.6)
    
    def create_comparison_chart(self, data_dict, save_path=None):
        """
        Create a comparison chart showing price data from multiple exchanges
        
        Args:
            data_dict (dict): Dictionary with exchange names as keys and DataFrames as values
            save_path (str): Path to save the chart (optional)
        
        Returns:
            str: Path to saved chart
        """
        fig, ax = plt.subplots(figsize=(16, 8))
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i, (exchange_name, df) in enumerate(data_dict.items()):
            if df is not None and len(df) > 0:
                color = colors[i % len(colors)]
                ax.plot(df.index, df['close'], label=exchange_name.upper(), 
                       color=color, linewidth=2, alpha=0.8)
        
        ax.set_title('BTC/USDT Price Comparison Across Exchanges', 
                    fontsize=14, fontweight='bold')
        ax.set_ylabel('Price (USDT)', fontsize=12)
        ax.set_xlabel('Date', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        # Save chart
        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(CHART_SAVE_PATH, f'comparison_{timestamp}.png')
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        
        print(f"Comparison chart saved: {save_path}")
        return save_path 