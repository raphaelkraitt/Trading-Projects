import config
from datetime import datetime

class Portfolio:
    def __init__(self):
        self.balance = config.INITIAL_BALANCE
        self.positions = {}  # symbol -> quantity
        self.trade_history = []
    
    def execute_trade(self, symbol, action, price, quantity):
        if action == 'BUY':
            cost = price * quantity
            if cost <= self.balance:
                self.balance -= cost
                self.positions[symbol] = self.positions.get(symbol, 0) + quantity
                self.trade_history.append({
                    'timestamp': datetime.now(),
                    'symbol': symbol,
                    'action': action,
                    'price': price,
                    'quantity': quantity,
                    'balance': self.balance
                })
                return True
        elif action == 'SELL':
            if symbol in self.positions and self.positions[symbol] >= quantity:
                revenue = price * quantity
                self.balance += revenue
                self.positions[symbol] -= quantity
                if self.positions[symbol] == 0:
                    del self.positions[symbol]
                self.trade_history.append({
                    'timestamp': datetime.now(),
                    'symbol': symbol,
                    'action': action,
                    'price': price,
                    'quantity': quantity,
                    'balance': self.balance
                })
                return True
        return False
    
    def get_pnl(self, current_prices):
        total_value = self.balance
        pnl = 0
        for symbol, quantity in self.positions.items():
            if symbol in current_prices:
                current_price = current_prices[symbol]['last']
                total_value += quantity * current_price
                # Calculate unrealized PnL (simplified)
                pnl += quantity * current_price
        return total_value, pnl
    
    def get_trade_history(self):
        return self.trade_history

if __name__ == "__main__":
    portfolio = Portfolio()
    print(f"Initial balance: ${portfolio.balance}")
    # Mock trade
    portfolio.execute_trade('BTC/USDT', 'BUY', 50000, 0.01)
    print(f"After trade: ${portfolio.balance}")
    print(f"Positions: {portfolio.positions}") 