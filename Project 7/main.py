import config
from mt5_portfolio import MT5Portfolio
from optimizer import mean_variance_optimization
from rebalancer import calculate_rebalance
from chart_generator import plot_portfolio_allocation
import numpy as np
import time

def main():
    print("\n=== Portfolio Rebalancer for Stocks (MT5) ===\n")
    portfolio = MT5Portfolio()
    # Step 1: Get current holdings
    holdings = portfolio.get_holdings()
    print("Current Holdings:", holdings)
    # Step 2: Fetch historical prices
    price_dfs = {s: portfolio.fetch_ohlcv(s) for s in config.PORTFOLIO_SYMBOLS}
    # Step 3: Get latest prices
    latest_prices = {s: df['Close'].iloc[-1] for s, df in price_dfs.items() if not df.empty}
    print("Latest Prices:", latest_prices)
    # Step 4: Mean-variance optimization
    optimal_weights, result = mean_variance_optimization(price_dfs, risk_free_rate=config.RISK_FREE_RATE)
    print("Optimal Weights:", optimal_weights)
    # Step 5: Calculate total portfolio value
    total_value = sum(holdings.get(s, 0) * latest_prices.get(s, 0) for s in config.PORTFOLIO_SYMBOLS)
    print(f"Total Portfolio Value: ${total_value:.2f}")
    # Step 6: Calculate suggested trades
    trades = calculate_rebalance(holdings, latest_prices, optimal_weights, total_value)
    print("\nSuggested Trades (positive: buy, negative: sell):")
    for s, qty in trades.items():
        print(f"  {s}: {qty:+.2f} shares")
    # Step 7: Visualize allocation
    chart_path = plot_portfolio_allocation(optimal_weights, save=True)
    print(f"\nSaved portfolio allocation chart: {chart_path}")
    portfolio.shutdown()
    print("\nDone.")

if __name__ == "__main__":
    main() 