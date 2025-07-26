import pandas as pd
import numpy as np
import config

def run_backtest(df: pd.DataFrame) -> pd.DataFrame:
    balance = config.INITIAL_BALANCE
    position = 0  # BTC
    equity_curve = []
    trades = []
    for i, row in df.iterrows():
        price = row['close']
        signal = row['signal']
        # Entry
        if signal == 1 and position == 0:
            position = config.TRADE_SIZE
            balance -= price * config.TRADE_SIZE * (1 + config.FEE)
            trades.append({'datetime': row['datetime'], 'action': 'BUY', 'price': price, 'balance': balance})
        # Exit
        elif signal == -1 and position > 0:
            balance += price * position * (1 - config.FEE)
            trades.append({'datetime': row['datetime'], 'action': 'SELL', 'price': price, 'balance': balance})
            position = 0
        # Track equity
        equity = balance + position * price
        equity_curve.append({'datetime': row['datetime'], 'equity': equity})
    return pd.DataFrame(trades), pd.DataFrame(equity_curve)

def calculate_performance(equity_df: pd.DataFrame) -> dict:
    returns = equity_df['equity'].pct_change().dropna()
    total_return = (equity_df['equity'].iloc[-1] / equity_df['equity'].iloc[0]) - 1
    max_drawdown = ((equity_df['equity'].cummax() - equity_df['equity']) / equity_df['equity'].cummax()).max()
    sharpe = returns.mean() / returns.std() * np.sqrt(252*24) if returns.std() > 0 else 0  # Annualized
    return {
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe
    }

if __name__ == "__main__":
    import data_fetcher, strategy
    df = data_fetcher.load_ohlcv()
    df = strategy.add_sma_signals(df)
    trades, equity = run_backtest(df)
    perf = calculate_performance(equity)
    print(perf)
    print(trades.tail()) 