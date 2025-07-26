import data_fetcher
import indicators
import trading_bot
import chart_generator
import config
import pandas as pd
import os

def main():
    print("\n=== Stock Momentum Trading Bot with MT5 ===\n")
    # Step 1: Fetch data
    fetcher = data_fetcher.MT5DataFetcher()
    df = fetcher.fetch_ohlcv()
    fetcher.shutdown()
    if df.empty:
        print("No data fetched. Exiting.")
        return
    print(f"Fetched {len(df)} bars of {config.SYMBOL} data.")
    # Step 2: Add indicators
    df = indicators.add_indicators(df)
    print("Indicators calculated.")
    # Step 3: Simulate trading
    bot = trading_bot.SimulatedTradingBot()
    trades = bot.run(df)
    equity = bot.get_equity_curve()
    print(f"Simulated {len(trades)} trades.")
    # Step 4: Generate charts
    price_chart = chart_generator.plot_price_rsi_macd(df, trades, save=True)
    equity_chart = chart_generator.plot_equity_curve(equity, save=True)
    print(f"Saved price/indicator chart: {os.path.basename(price_chart)}")
    print(f"Saved equity curve chart: {os.path.basename(equity_chart)}")
    # Step 5: Print summary
    if not trades.empty:
        print("\nTrade Log:")
        print(trades.tail())
    print("\nDone.")

if __name__ == "__main__":
    main() 