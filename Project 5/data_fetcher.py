import ccxt
import pandas as pd
import os
import config

def fetch_binance_ohlcv(symbol=None, timeframe=None, limit=None, save_path=None) -> pd.DataFrame:
    symbol = symbol or config.SYMBOL
    timeframe = timeframe or config.TIMEFRAME
    limit = limit or config.HIST_BARS
    save_path = save_path or config.DATA_PATH
    exchange = ccxt.binance()
    print(f"Fetching {symbol} {timeframe} data from Binance...")
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    df.to_csv(save_path, index=False)
    print(f"Saved data to {save_path}")
    return df

def load_ohlcv(path=None) -> pd.DataFrame:
    path = path or config.DATA_PATH
    if os.path.exists(path):
        df = pd.read_csv(path, parse_dates=['datetime'])
        return df
    else:
        return fetch_binance_ohlcv(save_path=path)

if __name__ == "__main__":
    df = fetch_binance_ohlcv()
    print(df.tail()) 