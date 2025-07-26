import pandas as pd
import config

def add_sma_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['sma_fast'] = df['close'].rolling(config.SMA_FAST).mean()
    df['sma_slow'] = df['close'].rolling(config.SMA_SLOW).mean()
    df['signal'] = 0
    df.loc[df['sma_fast'] > df['sma_slow'], 'signal'] = 1  # Long
    df.loc[df['sma_fast'] < df['sma_slow'], 'signal'] = -1  # Short/exit
    df['signal'] = df['signal'].shift(1).fillna(0)  # Trade on next bar
    return df

if __name__ == "__main__":
    import data_fetcher
    df = data_fetcher.load_ohlcv()
    df = add_sma_signals(df)
    print(df[['datetime', 'close', 'sma_fast', 'sma_slow', 'signal']].tail()) 