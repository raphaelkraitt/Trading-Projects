import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import config

class MT5Trader:
    def __init__(self):
        self.connected = False
        self.last_signal_time = None
        self.trade_history = []
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
        
        # Optional login
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
    
    def get_current_price(self, symbol=None):
        symbol = symbol or config.SYMBOL
        if not self.connected:
            return None
        
        tick = mt5.symbol_info_tick(symbol)
        if tick:
            return (tick.bid + tick.ask) / 2  # Mid price
        return None
    
    def generate_signal(self, sentiment_score):
        """Generate trading signal based on sentiment score"""
        current_time = datetime.now()
        
        # Check cooldown period
        if self.last_signal_time:
            time_since_last = current_time - self.last_signal_time
            if time_since_last < timedelta(hours=config.SIGNAL_COOLDOWN_HOURS):
                return None
        
        # Generate signal based on sentiment thresholds
        if sentiment_score >= config.SENTIMENT_THRESHOLD_BUY:
            signal = "BUY"
        elif sentiment_score <= config.SENTIMENT_THRESHOLD_SELL:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        if signal != "HOLD":
            self.last_signal_time = current_time
        
        return signal
    
    def simulate_trade(self, signal, sentiment_score, price):
        """Simulate a trade (does not place real orders)"""
        if signal in ["BUY", "SELL"]:
            trade = {
                'timestamp': datetime.now(),
                'signal': signal,
                'sentiment_score': sentiment_score,
                'price': price,
                'quantity': config.TRADE_SIZE,
                'value': price * config.TRADE_SIZE
            }
            self.trade_history.append(trade)
            print(f"Simulated {signal} order: {config.TRADE_SIZE} shares at ${price:.2f}")
            return trade
        return None
    
    def get_trade_history(self):
        return pd.DataFrame(self.trade_history)
    
    def shutdown(self):
        mt5.shutdown()
        self.connected = False

if __name__ == "__main__":
    trader = MT5Trader()
    price = trader.get_current_price()
    print(f"Current {config.SYMBOL} price: ${price}")
    
    # Test signal generation
    test_sentiments = [0.5, -0.3, 0.1, -0.8]
    for sentiment in test_sentiments:
        signal = trader.generate_signal(sentiment)
        print(f"Sentiment: {sentiment:.2f} -> Signal: {signal}")
    
    trader.shutdown() 