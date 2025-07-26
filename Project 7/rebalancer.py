import config
import numpy as np
import pandas as pd

def calculate_rebalance(current_holdings, prices, optimal_weights, total_value):
    # Calculate target value for each asset
    targets = {s: optimal_weights[s] * total_value for s in optimal_weights}
    # Calculate current value for each asset
    current_values = {s: current_holdings.get(s, 0) * prices[s] for s in optimal_weights}
    # Calculate difference (positive: buy, negative: sell)
    trades = {s: (targets[s] - current_values[s]) / prices[s] for s in optimal_weights}
    return trades

if __name__ == "__main__":
    # Example usage
    current_holdings = {'AAPL': 10, 'MSFT': 5, 'GOOGL': 2, 'AMZN': 1, 'TSLA': 3}
    prices = {'AAPL': 170, 'MSFT': 320, 'GOOGL': 2800, 'AMZN': 3400, 'TSLA': 700}
    optimal_weights = {'AAPL': 0.2, 'MSFT': 0.2, 'GOOGL': 0.2, 'AMZN': 0.2, 'TSLA': 0.2}
    total_value = sum(current_holdings[s] * prices[s] for s in current_holdings)
    trades = calculate_rebalance(current_holdings, prices, optimal_weights, total_value)
    print("Suggested trades:", trades) 