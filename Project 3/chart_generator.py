import matplotlib.pyplot as plt
import pandas as pd
import os
import config

def plot_price_rsi_macd(df: pd.DataFrame, trades: pd.DataFrame = None, save: bool = True) -> str:
    """Plot price, RSI, MACD overlays, and mark trades. Save chart if requested."""
    if df.empty:
        return ""
    fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True, gridspec_kw={'height_ratios': [2, 1, 1]})
    # Price
    axes[0].plot(df['datetime'], df['Close'], label='Close Price', color='black')
    axes[0].set_title(f"{config.SYMBOL} Price with Trades")
    axes[0].set_ylabel('Price')
    # Mark trades
    if trades is not None and not trades.empty:
        buys = trades[trades['action'] == 'BUY']
        sells = trades[trades['action'] == 'SELL']
        axes[0].scatter(buys['datetime'], buys['price'], marker='^', color='green', s=100, label='Buy', zorder=5)
        axes[0].scatter(sells['datetime'], sells['price'], marker='v', color='red', s=100, label='Sell', zorder=5)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    # RSI
    axes[1].plot(df['datetime'], df['RSI'], label='RSI', color='blue')
    axes[1].axhline(config.RSI_OVERBOUGHT, color='red', linestyle='--', label='Overbought')
    axes[1].axhline(config.RSI_OVERSOLD, color='green', linestyle='--', label='Oversold')
    axes[1].set_ylabel('RSI')
    axes[1].set_title('RSI')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    # MACD
    axes[2].plot(df['datetime'], df['MACD'], label='MACD', color='purple')
    axes[2].plot(df['datetime'], df['MACD_signal'], label='Signal', color='orange')
    axes[2].bar(df['datetime'], df['MACD_diff'], label='MACD Diff', color='gray', alpha=0.5)
    axes[2].set_ylabel('MACD')
    axes[2].set_title('MACD')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    plt.tight_layout()
    if save:
        if not os.path.exists(config.CHART_SAVE_PATH):
            os.makedirs(config.CHART_SAVE_PATH)
        filename = f"{config.SYMBOL}_momentum_chart_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.{config.CHART_FORMAT}"
        filepath = os.path.join(config.CHART_SAVE_PATH, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        return filepath
    else:
        plt.show()
        return ""

def plot_equity_curve(equity_df: pd.DataFrame, save: bool = True) -> str:
    if equity_df.empty:
        return ""
    plt.figure(figsize=(14, 6))
    plt.plot(equity_df['datetime'], equity_df['equity'], label='Equity Curve', color='navy')
    plt.title('Simulated Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Equity ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    if save:
        if not os.path.exists(config.CHART_SAVE_PATH):
            os.makedirs(config.CHART_SAVE_PATH)
        filename = f"equity_curve_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.{config.CHART_FORMAT}"
        filepath = os.path.join(config.CHART_SAVE_PATH, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        return filepath
    else:
        plt.show()
        return ""

if __name__ == "__main__":
    import data_fetcher
    import indicators
    import trading_bot
    fetcher = data_fetcher.MT5DataFetcher()
    df = fetcher.fetch_ohlcv()
    fetcher.shutdown()
    df = indicators.add_indicators(df)
    bot = trading_bot.SimulatedTradingBot()
    trades = bot.run(df)
    eq = bot.get_equity_curve()
    print(plot_price_rsi_macd(df, trades, save=False))
    print(plot_equity_curve(eq, save=False)) 