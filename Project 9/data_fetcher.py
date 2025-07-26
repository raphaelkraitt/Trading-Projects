import ccxt
import config
from datetime import datetime

class LiveDataFetcher:
    def __init__(self):
        self.exchange = ccxt.binance()
    
    def get_ticker(self, symbol):
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'last': ticker['last'],
                'volume': ticker['baseVolume'],
                'timestamp': datetime.now()
            }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
    
    def get_all_tickers(self):
        tickers = {}
        for symbol in config.SYMBOLS:
            ticker = self.get_ticker(symbol)
            if ticker:
                tickers[symbol] = ticker
        return tickers

if __name__ == "__main__":
    fetcher = LiveDataFetcher()
    tickers = fetcher.get_all_tickers()
    for symbol, data in tickers.items():
        print(f"{symbol}: ${data['last']:.2f}") 