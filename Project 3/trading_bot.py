import pandas as pd
import config

class SimulatedTradingBot:
    def __init__(self, initial_balance=None, trade_size=None):
        self.balance = initial_balance if initial_balance is not None else config.INITIAL_BALANCE
        self.trade_size = trade_size if trade_size is not None else config.TRADE_SIZE
        self.position = 0  # Number of shares held
        self.trades = []
        self.equity_curve = []

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """Run the trading simulation on the dataframe with indicators."""
        for i, row in df.iterrows():
            price = row['Close']
            rsi = row['RSI']
            date = row['datetime']
            action = None
            # Buy signal
            if rsi <= config.RSI_OVERSOLD and self.position == 0:
                self.position += self.trade_size
                self.balance -= price * self.trade_size
                action = 'BUY'
                self.trades.append({'datetime': date, 'action': action, 'price': price, 'rsi': rsi, 'position': self.position, 'balance': self.balance})
            # Sell signal
            elif rsi >= config.RSI_OVERBOUGHT and self.position > 0:
                self.position -= self.trade_size
                self.balance += price * self.trade_size
                action = 'SELL'
                self.trades.append({'datetime': date, 'action': action, 'price': price, 'rsi': rsi, 'position': self.position, 'balance': self.balance})
            # Track equity
            equity = self.balance + self.position * price
            self.equity_curve.append({'datetime': date, 'equity': equity})
        return pd.DataFrame(self.trades)

    def get_equity_curve(self) -> pd.DataFrame:
        return pd.DataFrame(self.equity_curve)

if __name__ == "__main__":
    import data_fetcher
    import indicators
    fetcher = data_fetcher.MT5DataFetcher()
    df = fetcher.fetch_ohlcv()
    fetcher.shutdown()
    df = indicators.add_indicators(df)
    bot = SimulatedTradingBot()
    trades = bot.run(df)
    print(trades)
    print(bot.get_equity_curve().tail()) 