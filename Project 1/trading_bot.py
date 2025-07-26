import pandas as pd
import numpy as np
from datetime import datetime
import time
import os

from data_fetcher import DataFetcher
from signal_generator import SignalGenerator
from chart_generator import ChartGenerator
from config import SYMBOL, TIMEFRAME, LIMIT

class TradingBot:
    def __init__(self):
        """Initialize the trading bot with all components"""
        self.data_fetcher = DataFetcher()
        self.signal_generator = SignalGenerator()
        self.chart_generator = ChartGenerator()
        self.data = {}
        self.processed_data = {}
        
    def fetch_data(self, symbol=SYMBOL, timeframe=TIMEFRAME, limit=LIMIT):
        """
        Fetch data from all exchanges
        
        Args:
            symbol (str): Trading pair symbol
            timeframe (str): Timeframe for data
            limit (int): Number of candles to fetch
        
        Returns:
            dict: Dictionary with exchange data
        """
        print(f"\n🔄 Fetching {symbol} data from exchanges...")
        self.data = self.data_fetcher.fetch_all_exchanges(symbol, timeframe, limit)
        return self.data
    
    def process_data(self):
        """
        Process data and calculate indicators and signals
        
        Returns:
            dict: Dictionary with processed data
        """
        print("\n📊 Processing data and calculating indicators...")
        self.processed_data = {}
        
        for exchange_name, df in self.data.items():
            if df is not None and len(df) > 0:
                print(f"Processing {exchange_name} data...")
                
                # Calculate indicators
                df_with_indicators = self.signal_generator.calculate_indicators(df.copy())
                
                # Generate signals
                df_with_signals = self.signal_generator.generate_signals(df_with_indicators)
                
                self.processed_data[exchange_name] = df_with_signals
                print(f"✓ Processed {exchange_name} data")
            else:
                print(f"✗ No data available for {exchange_name}")
        
        return self.processed_data
    
    def generate_charts(self):
        """
        Generate charts for all exchanges
        
        Returns:
            list: List of saved chart paths
        """
        print("\n📈 Generating charts...")
        chart_paths = []
        
        for exchange_name, df in self.processed_data.items():
            if df is not None and len(df) > 0:
                print(f"Creating chart for {exchange_name}...")
                chart_path = self.chart_generator.create_candlestick_chart(df, exchange_name)
                if chart_path:
                    chart_paths.append(chart_path)
        
        # Create comparison chart
        if len(self.data) > 1:
            print("Creating comparison chart...")
            comparison_path = self.chart_generator.create_comparison_chart(self.data)
            if comparison_path:
                chart_paths.append(comparison_path)
        
        return chart_paths
    
    def get_latest_signals(self):
        """
        Get latest signals from all exchanges
        
        Returns:
            dict: Dictionary with latest signals for each exchange
        """
        latest_signals = {}
        
        for exchange_name, df in self.processed_data.items():
            if df is not None and len(df) > 0:
                signals = self.signal_generator.get_latest_signals(df)
                latest_signals[exchange_name] = signals
        
        return latest_signals
    
    def get_signal_summary(self):
        """
        Get signal summary for all exchanges
        
        Returns:
            dict: Dictionary with signal summaries for each exchange
        """
        signal_summaries = {}
        
        for exchange_name, df in self.processed_data.items():
            if df is not None and len(df) > 0:
                summary = self.signal_generator.get_signal_summary(df)
                signal_summaries[exchange_name] = summary
        
        return signal_summaries
    
    def print_latest_signals(self):
        """Print latest signals in a formatted way"""
        latest_signals = self.get_latest_signals()
        
        print("\n" + "="*80)
        print("📊 LATEST TRADING SIGNALS")
        print("="*80)
        
        for exchange_name, signals in latest_signals.items():
            print(f"\n🔸 {exchange_name.upper()}:")
            print(f"   Timestamp: {signals['timestamp']}")
            print(f"   Current Price: ${signals['price']:,.2f}")
            print(f"   Recommendation: {signals['recommendation']}")
            print(f"   SMA Signal: {signals['sma_signal']}")
            print(f"   EMA Signal: {signals['ema_signal']}")
            print(f"   RSI Signal: {signals['rsi_signal']}")
            print(f"   BB Signal: {signals['bb_signal']}")
            print(f"   Combined Signal: {signals['combined_signal']:.4f}")
    
    def print_signal_summary(self):
        """Print signal summary in a formatted way"""
        signal_summaries = self.get_signal_summary()
        
        print("\n" + "="*80)
        print("📈 SIGNAL SUMMARY")
        print("="*80)
        
        for exchange_name, summary in signal_summaries.items():
            print(f"\n🔸 {exchange_name.upper()}:")
            print(f"   Total Periods: {summary['total_periods']}")
            print(f"   Buy Signals: {summary['buy_signals']} ({summary['buy_percentage']:.1f}%)")
            print(f"   Sell Signals: {summary['sell_signals']} ({summary['sell_percentage']:.1f}%)")
            print(f"   Hold Signals: {summary['hold_signals']} ({summary['hold_percentage']:.1f}%)")
    
    def run_analysis(self):
        """
        Run complete analysis: fetch data, process, generate charts, and display results
        
        Returns:
            dict: Analysis results
        """
        print("🚀 Starting Trading Bot Analysis...")
        print("="*80)
        
        # Fetch data
        self.fetch_data()
        
        if not self.data:
            print("❌ No data fetched from any exchange. Please check your API keys and internet connection.")
            return None
        
        # Process data
        self.process_data()
        
        if not self.processed_data:
            print("❌ No data processed. Please check your data.")
            return None
        
        # Generate charts
        chart_paths = self.generate_charts()
        
        # Display results
        self.print_latest_signals()
        self.print_signal_summary()
        
        # Print chart information
        if chart_paths:
            print(f"\n📊 Generated {len(chart_paths)} charts:")
            for path in chart_paths:
                print(f"   📁 {path}")
        
        print("\n✅ Analysis complete!")
        
        return {
            'data': self.data,
            'processed_data': self.processed_data,
            'latest_signals': self.get_latest_signals(),
            'signal_summary': self.get_signal_summary(),
            'chart_paths': chart_paths
        }
    
    def get_exchange_info(self):
        """
        Get information about all exchanges
        
        Returns:
            dict: Exchange information
        """
        exchange_info = {}
        
        for exchange_name in self.data_fetcher.exchanges.keys():
            info = self.data_fetcher.get_exchange_info(exchange_name)
            if info:
                exchange_info[exchange_name] = info
        
        return exchange_info
    
    def print_exchange_info(self):
        """Print exchange information in a formatted way"""
        exchange_info = self.get_exchange_info()
        
        print("\n" + "="*80)
        print("🏢 EXCHANGE INFORMATION")
        print("="*80)
        
        for exchange_name, info in exchange_info.items():
            print(f"\n🔸 {exchange_name.upper()}:")
            print(f"   Current Price: ${info['current_price']:,.2f}")
            print(f"   24h Volume: {info['24h_volume']:,.2f} BTC")
            print(f"   24h Change: {info['24h_change']:+.2f}%")
            print(f"   Available Symbols: {len(info['symbols'])}") 