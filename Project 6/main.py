import time
import config
from arbitrage_bot import ArbitrageBot
import matplotlib.pyplot as plt
import os

def main():
    print("\n=== Arbitrage Bot: Binance vs MEXC ===\n")
    bot = ArbitrageBot()
    num_cycles = 30  # Number of price checks (simulate real-time)
    interval = 5  # seconds between checks
    for i in range(num_cycles):
        print(f"Cycle {i+1}/{num_cycles}")
        bot.run_once()
        time.sleep(interval)
    # Plot equity curve
    equity = bot.get_equity_curve()
    if not equity.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(equity['timestamp'], equity['equity'], marker='o', color='navy')
        plt.title('Arbitrage Bot Simulated Profit/Loss')
        plt.xlabel('Time')
        plt.ylabel('Equity (USDT)')
        plt.grid(True, alpha=0.3)
        if not os.path.exists(config.CHART_SAVE_PATH):
            os.makedirs(config.CHART_SAVE_PATH)
        filename = f"arbitrage_equity_curve.{config.CHART_FORMAT}"
        filepath = os.path.join(config.CHART_SAVE_PATH, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved equity curve chart: {filepath}")
    # Print trade log
    trades = bot.get_trade_log()
    if not trades.empty:
        print("\nTrade Log:")
        print(trades.tail())
    print("\nDone.")

if __name__ == "__main__":
    main() 