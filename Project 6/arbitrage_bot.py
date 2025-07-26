import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import config

class ArbitrageBot:
    def __init__(self):
        self.binance = ccxt.binance()
        self.mexc = ccxt.mexc()
        self.balance = config.INITIAL_BALANCE
        self.position = 0  # BTC
        self.trade_log = []
        self.equity_curve = []

    def fetch_prices(self):
        binance_ticker = self.binance.fetch_ticker(config.SYMBOL)
        mexc_ticker = self.mexc.fetch_ticker(config.SYMBOL)
        return {
            'timestamp': datetime.utcnow(),
            'binance_bid': binance_ticker['bid'],
            'binance_ask': binance_ticker['ask'],
            'mexc_bid': mexc_ticker['bid'],
            'mexc_ask': mexc_ticker['ask']
        }

    def detect_arbitrage(self, prices):
        # Buy on cheaper, sell on more expensive (after fees)
        # Opportunity 1: Buy Binance, Sell MEXC
        buy_price = prices['binance_ask'] * (1 + config.BINANCE_FEE)
        sell_price = prices['mexc_bid'] * (1 - config.MEXC_FEE)
        profit1 = (sell_price - buy_price) * config.TRADE_AMOUNT
        # Opportunity 2: Buy MEXC, Sell Binance
        buy_price2 = prices['mexc_ask'] * (1 + config.MEXC_FEE)
        sell_price2 = prices['binance_bid'] * (1 - config.BINANCE_FEE)
        profit2 = (sell_price2 - buy_price2) * config.TRADE_AMOUNT
        if profit1 > config.MIN_PROFIT_USDT:
            return 'BINANCE->MEXC', profit1
        elif profit2 > config.MIN_PROFIT_USDT:
            return 'MEXC->BINANCE', profit2
        else:
            return None, 0

    def simulate_trade(self, direction, profit, prices):
        self.balance += profit
        self.trade_log.append({
            'timestamp': prices['timestamp'],
            'direction': direction,
            'profit': profit,
            'balance': self.balance
        })
        self.equity_curve.append({'timestamp': prices['timestamp'], 'equity': self.balance})

    def run_once(self):
        prices = self.fetch_prices()
        direction, profit = self.detect_arbitrage(prices)
        if direction:
            self.simulate_trade(direction, profit, prices)
            print(f"Arbitrage: {direction} | Profit: {profit:.2f} USDT | New Balance: {self.balance:.2f}")
        else:
            print(f"No arbitrage opportunity. Balance: {self.balance:.2f}")
        return prices, direction, profit

    def get_trade_log(self):
        return pd.DataFrame(self.trade_log)

    def get_equity_curve(self):
        return pd.DataFrame(self.equity_curve)

if __name__ == "__main__":
    bot = ArbitrageBot()
    for _ in range(10):
        bot.run_once()
    print(bot.get_trade_log()) 