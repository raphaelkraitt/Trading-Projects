import data_fetcher
import strategy
import backtester
import chart_generator
import config


def main():
    print("\n=== Crypto Backtesting Framework (BTC/USDT) ===\n")
    # Step 1: Load data
    df = data_fetcher.load_ohlcv()
    print(f"Loaded {len(df)} bars of {config.SYMBOL} data.")
    # Step 2: Add strategy signals
    df = strategy.add_sma_signals(df)
    print("SMA signals calculated.")
    # Step 3: Run backtest
    trades, equity = backtester.run_backtest(df)
    print(f"Simulated {len(trades)} trades.")
    # Step 4: Calculate performance
    perf = backtester.calculate_performance(equity)
    print("\nPerformance Metrics:")
    print(f"  Total Return: {perf['total_return']*100:.2f}%")
    print(f"  Max Drawdown: {perf['max_drawdown']*100:.2f}%")
    print(f"  Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
    # Step 5: Plot equity curve
    chart_path = chart_generator.plot_equity_curve(equity, save=True)
    print(f"\nSaved equity curve chart: {chart_path}")
    # Step 6: Print trade log
    if not trades.empty:
        print("\nTrade Log:")
        print(trades.tail())
    print("\nDone.")

if __name__ == "__main__":
    main() 