import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import config

class MT5DataFetcher:
    def __init__(self):
        self.connected = False
        self._connect()
    
    def _connect(self):
        if config.MT5_PATH:
            mt5.initialize(path=config.MT5_PATH)
        else:
            mt5.initialize()
        if mt5.version():
            self.connected = True
            print(f"MT5 initialized: {mt5.version()}")
        else:
            print("Failed to initialize MT5")
            self.connected = False
        # Optional login for real/demo accounts
        if config.MT5_LOGIN and config.MT5_PASSWORD and config.MT5_SERVER:
            authorized = mt5.login(
                login=int(config.MT5_LOGIN),
                password=config.MT5_PASSWORD,
                server=config.MT5_SERVER
            )
            if authorized:
                print("MT5 login successful")
            else:
                print("MT5 login failed")
    
    def fetch_ohlcv(self, symbol=None, timeframe=None, bars=None) -> pd.DataFrame:
        if not self.connected:
            print("MT5 not connected")
            return pd.DataFrame()
        symbol = symbol or config.SYMBOL
        timeframe = timeframe or config.TIMEFRAME
        bars = bars or config.HIST_BARS
        tf_map = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1
        }
        tf = tf_map.get(timeframe, mt5.TIMEFRAME_H1)
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
        if rates is None or len(rates) == 0:
            print(f"No data for {symbol} {timeframe}")
            return pd.DataFrame()
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.rename(columns={'time': 'datetime', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'tick_volume': 'Volume'})
        df = df[['datetime', 'Open', 'High', 'Low', 'Close', 'Volume']]
        return df
    
    def shutdown(self):
        mt5.shutdown()
        self.connected = False

if __name__ == "__main__":
    fetcher = MT5DataFetcher()
    df = fetcher.fetch_ohlcv()
    print(df.tail())
    fetcher.shutdown() 