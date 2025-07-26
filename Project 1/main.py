#!/usr/bin/env python3
"""
Crypto Trading Bot
==================

A Python trading bot that connects to Binance and MEXC, fetches BTC/USDT data,
calculates technical indicators, generates buy/sell signals, and creates charts.

Features:
- Multi-exchange data fetching (Binance, MEXC)
- Technical indicators (SMA, EMA, RSI, Bollinger Bands)
- Signal generation based on crossovers
- Chart generation with indicators
- Signal analysis and summary

Author: Trading Bot
Version: 1.0.0
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trading_bot import TradingBot
from config import SYMBOL, TIMEFRAME, LIMIT

def print_banner():
    """Print the bot banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🚀 CRYPTO TRADING BOT 🚀                   ║
    ║                                                              ║
    ║  • Multi-exchange data fetching (Binance, MEXC)             ║
    ║  • Technical indicators (SMA, EMA, RSI, Bollinger Bands)    ║
    ║  • Signal generation based on crossovers                    ║
    ║  • Chart generation with indicators                         ║
    ║  • Signal analysis and summary                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_config():
    """Print current configuration"""
    print("📋 Current Configuration:")
    print(f"   Symbol: {SYMBOL}")
    print(f"   Timeframe: {TIMEFRAME}")
    print(f"   Data Limit: {LIMIT} candles")
    print(f"   Exchanges: Binance, MEXC")
    print()

def main():
    """Main function to run the trading bot"""
    print_banner()
    print_config()
    
    # Initialize trading bot
    bot = TradingBot()
    
    try:
        # Run complete analysis
        results = bot.run_analysis()
        
        if results is None:
            print("❌ Analysis failed. Please check your configuration and try again.")
            return
        
        # Print exchange information
        bot.print_exchange_info()
        
        print("\n" + "="*80)
        print("🎉 Trading Bot Analysis Complete!")
        print("="*80)
        print(f"📅 Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Charts saved in: {os.path.abspath('charts')}")
        print("\n💡 Tips:")
        print("   • Review the generated charts for visual analysis")
        print("   • Check the signal summary for trading opportunities")
        print("   • Monitor the latest signals for current recommendations")
        print("   • Always do your own research before making trading decisions")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user.")
        print("Thank you for using the Crypto Trading Bot!")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please check your configuration and try again.")
        
        # Print helpful debugging information
        print("\n🔧 Debugging Tips:")
        print("   • Check your API keys in .env file")
        print("   • Ensure you have internet connection")
        print("   • Verify exchange API endpoints are accessible")
        print("   • Check if the trading pair is available on exchanges")

def run_demo():
    """Run a demo with sample data (for testing without API keys)"""
    print("🧪 Running in demo mode...")
    print("This mode uses sample data for demonstration purposes.")
    print("For real trading, please configure your API keys in .env file.\n")
    
    # Import demo data generator
    try:
        from demo_data import generate_demo_data
        from trading_bot import TradingBot
        
        # Generate demo data
        demo_data = generate_demo_data()
        
        # Initialize bot
        bot = TradingBot()
        bot.data = demo_data
        
        # Process demo data
        bot.process_data()
        
        # Generate charts
        chart_paths = bot.generate_charts()
        
        # Display results
        bot.print_latest_signals()
        bot.print_signal_summary()
        
        print(f"\n📊 Generated {len(chart_paths)} demo charts:")
        for path in chart_paths:
            print(f"   📁 {path}")
            
    except ImportError:
        print("❌ Demo mode not available. Please install all dependencies.")

if __name__ == "__main__":
    # Check if running in demo mode
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        main() 