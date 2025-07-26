import matplotlib.pyplot as plt
import os
import config

def plot_equity_curve(equity_df, save=True):
    plt.figure(figsize=(14, 6))
    plt.plot(equity_df['datetime'], equity_df['equity'], color='navy', label='Equity Curve')
    plt.title('Backtest Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Equity (USDT)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    if save:
        if not os.path.exists(config.CHART_SAVE_PATH):
            os.makedirs(config.CHART_SAVE_PATH)
        filename = f"backtest_equity_curve.{config.CHART_FORMAT}"
        filepath = os.path.join(config.CHART_SAVE_PATH, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        return filepath
    else:
        plt.show()
        return ""

if __name__ == "__main__":
    import data_fetcher, strategy, backtester
    df = data_fetcher.load_ohlcv()
    df = strategy.add_sma_signals(df)
    trades, equity = backtester.run_backtest(df)
    print(plot_equity_curve(equity, save=False)) 