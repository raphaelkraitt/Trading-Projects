import pandas as pd
import ta
import config

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add RSI and MACD columns to the dataframe."""
    df = df.copy()
    # RSI
    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=config.RSI_PERIOD).rsi()
    # MACD
    macd = ta.trend.MACD(
        close=df['Close'],
        window_slow=config.MACD_SLOW,
        window_fast=config.MACD_FAST,
        window_sign=config.MACD_SIGNAL
    )
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    df['MACD_diff'] = macd.macd_diff()
    return df

if __name__ == "__main__":
    # Example usage
    import data_fetcher
    fetcher = data_fetcher.MT5DataFetcher()
    df = fetcher.fetch_ohlcv()
    fetcher.shutdown()
    df = add_indicators(df)
    print(df.tail()) 