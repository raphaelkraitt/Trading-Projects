import MetaTrader5 as mt5
import pandas as pd
import config
from datetime import datetime, timedelta

class MT5Portfolio:
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
    def get_holdings(self):
        positions = mt5.positions_get()
        holdings = {}
        if positions:
            for pos in positions:
                symbol = pos.symbol
                volume = pos.volume
                if symbol in config.PORTFOLIO_SYMBOLS:
                    holdings[symbol] = holdings.get(symbol, 0) + volume
        return holdings
    def fetch_ohlcv(self, symbol, bars=None):
        bars = bars or config.HIST_BARS
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, bars)
        if rates is None or len(rates) == 0:
            print(f"No data for {symbol}")
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
    portfolio = MT5Portfolio()
    holdings = portfolio.get_holdings()
    print("Holdings:", holdings)
    for symbol in config.PORTFOLIO_SYMBOLS:
        df = portfolio.fetch_ohlcv(symbol)
        print(f"{symbol} last 5 days:")
        print(df.tail())
    portfolio.shutdown() 