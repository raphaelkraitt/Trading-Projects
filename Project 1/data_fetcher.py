import ccxt
import pandas as pd
from datetime import datetime
import time
from config import EXCHANGES, SYMBOL, TIMEFRAME, LIMIT

class DataFetcher:
    def __init__(self):
        self.exchanges = {}
        self.initialize_exchanges()
    
    def initialize_exchanges(self):
        """Initialize exchange connections"""
        for exchange_name, config in EXCHANGES.items():
            try:
                # Get exchange class
                exchange_class = getattr(ccxt, exchange_name)
                
                # Initialize exchange
                exchange = exchange_class({
                    'apiKey': config['api_key'],
                    'secret': config['secret'],
                    'sandbox': config['sandbox'],
                    'enableRateLimit': True,
                })
                
                self.exchanges[exchange_name] = exchange
                print(f"✓ {exchange_name.capitalize()} initialized successfully")
                
            except Exception as e:
                print(f"✗ Failed to initialize {exchange_name}: {str(e)}")
    
    def fetch_ohlcv(self, exchange_name, symbol=SYMBOL, timeframe=TIMEFRAME, limit=LIMIT):
        """
        Fetch OHLCV data from specified exchange
        
        Args:
            exchange_name (str): Name of the exchange
            symbol (str): Trading pair symbol
            timeframe (str): Timeframe for data
            limit (int): Number of candles to fetch
        
        Returns:
            pd.DataFrame: OHLCV data with datetime index
        """
        if exchange_name not in self.exchanges:
            raise ValueError(f"Exchange {exchange_name} not initialized")
        
        exchange = self.exchanges[exchange_name]
        
        try:
            # Fetch OHLCV data
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            # Convert timestamp to datetime
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('datetime', inplace=True)
            
            # Drop timestamp column
            df.drop('timestamp', axis=1, inplace=True)
            
            return df
            
        except Exception as e:
            print(f"Error fetching data from {exchange_name}: {str(e)}")
            return None
    
    def fetch_all_exchanges(self, symbol=SYMBOL, timeframe=TIMEFRAME, limit=LIMIT):
        """
        Fetch OHLCV data from all initialized exchanges
        
        Args:
            symbol (str): Trading pair symbol
            timeframe (str): Timeframe for data
            limit (int): Number of candles to fetch
        
        Returns:
            dict: Dictionary with exchange names as keys and DataFrames as values
        """
        data = {}
        
        for exchange_name in self.exchanges.keys():
            print(f"Fetching data from {exchange_name}...")
            df = self.fetch_ohlcv(exchange_name, symbol, timeframe, limit)
            
            if df is not None:
                data[exchange_name] = df
                print(f"✓ Fetched {len(df)} candles from {exchange_name}")
            else:
                print(f"✗ Failed to fetch data from {exchange_name}")
            
            # Rate limiting
            time.sleep(0.5)
        
        return data
    
    def get_exchange_info(self, exchange_name):
        """
        Get exchange information
        
        Args:
            exchange_name (str): Name of the exchange
        
        Returns:
            dict: Exchange information
        """
        if exchange_name not in self.exchanges:
            return None
        
        exchange = self.exchanges[exchange_name]
        
        try:
            markets = exchange.load_markets()
            ticker = exchange.fetch_ticker(SYMBOL)
            
            return {
                'name': exchange_name,
                'symbols': list(markets.keys()),
                'current_price': ticker['last'],
                '24h_volume': ticker['baseVolume'],
                '24h_change': ticker['percentage'],
            }
        except Exception as e:
            print(f"Error getting exchange info for {exchange_name}: {str(e)}")
            return None 