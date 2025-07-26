import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import config
from data_fetcher import LiveDataFetcher
from portfolio import Portfolio

class TradingDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Trading Dashboard")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        
        # Initialize components
        self.data_fetcher = LiveDataFetcher()
        self.portfolio = Portfolio()
        self.current_prices = {}
        
        # Create GUI
        self.create_widgets()
        
        # Start data updates
        self.update_data()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Crypto Trading Dashboard", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Price display frame
        price_frame = ttk.LabelFrame(main_frame, text="Live Prices", padding="10")
        price_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.price_labels = {}
        for i, symbol in enumerate(config.SYMBOLS):
            symbol_label = ttk.Label(price_frame, text=f"{symbol}:", font=('Arial', 12))
            symbol_label.grid(row=i, column=0, sticky=tk.W, padx=(0, 10))
            
            price_label = ttk.Label(price_frame, text="Loading...", font=('Arial', 12, 'bold'))
            price_label.grid(row=i, column=1, sticky=tk.W)
            self.price_labels[symbol] = price_label
        
        # Portfolio frame
        portfolio_frame = ttk.LabelFrame(main_frame, text="Portfolio", padding="10")
        portfolio_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.balance_label = ttk.Label(portfolio_frame, text=f"Balance: ${self.portfolio.balance:.2f}", font=('Arial', 12))
        self.balance_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.pnl_label = ttk.Label(portfolio_frame, text="PnL: $0.00", font=('Arial', 12))
        self.pnl_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # Trading frame
        trading_frame = ttk.LabelFrame(main_frame, text="Mock Trading", padding="10")
        trading_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        # Symbol selection
        ttk.Label(trading_frame, text="Symbol:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.symbol_var = tk.StringVar(value=config.SYMBOLS[0])
        symbol_combo = ttk.Combobox(trading_frame, textvariable=self.symbol_var, values=config.SYMBOLS, state="readonly")
        symbol_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=(0, 5))
        
        # Trade buttons
        button_frame = ttk.Frame(trading_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        buy_button = ttk.Button(button_frame, text="BUY", command=self.execute_buy, style="Buy.TButton")
        buy_button.grid(row=0, column=0, padx=(0, 10))
        
        sell_button = ttk.Button(button_frame, text="SELL", command=self.execute_sell, style="Sell.TButton")
        sell_button.grid(row=0, column=1)
        
        # Trade history frame
        history_frame = ttk.LabelFrame(main_frame, text="Trade History", padding="10")
        history_frame.grid(row=2, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Create treeview for trade history
        columns = ('Time', 'Symbol', 'Action', 'Price', 'Quantity', 'Balance')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        # Configure main frame grid weights
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def update_data(self):
        try:
            # Fetch new prices
            self.current_prices = self.data_fetcher.get_all_tickers()
            
            # Update price labels
            for symbol, data in self.current_prices.items():
                if symbol in self.price_labels:
                    self.price_labels[symbol].config(text=f"${data['last']:.2f}")
            
            # Update portfolio info
            total_value, pnl = self.portfolio.get_pnl(self.current_prices)
            self.balance_label.config(text=f"Balance: ${self.portfolio.balance:.2f}")
            self.pnl_label.config(text=f"Total Value: ${total_value:.2f}")
            
            # Update trade history
            self.update_trade_history()
            
        except Exception as e:
            print(f"Error updating data: {e}")
        
        # Schedule next update
        self.root.after(config.UPDATE_INTERVAL, self.update_data)
    
    def update_trade_history(self):
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add trade history
        for trade in self.portfolio.get_trade_history()[-10:]:  # Last 10 trades
            self.history_tree.insert('', 'end', values=(
                trade['timestamp'].strftime('%H:%M:%S'),
                trade['symbol'],
                trade['action'],
                f"${trade['price']:.2f}",
                trade['quantity'],
                f"${trade['balance']:.2f}"
            ))
    
    def execute_buy(self):
        symbol = self.symbol_var.get()
        if symbol in self.current_prices:
            price = self.current_prices[symbol]['last']
            success = self.portfolio.execute_trade(symbol, 'BUY', price, config.TRADE_SIZE)
            if success:
                messagebox.showinfo("Success", f"Bought {config.TRADE_SIZE} {symbol} at ${price:.2f}")
            else:
                messagebox.showerror("Error", "Insufficient balance")
        else:
            messagebox.showerror("Error", "No price data available")
    
    def execute_sell(self):
        symbol = self.symbol_var.get()
        if symbol in self.current_prices:
            price = self.current_prices[symbol]['last']
            success = self.portfolio.execute_trade(symbol, 'SELL', price, config.TRADE_SIZE)
            if success:
                messagebox.showinfo("Success", f"Sold {config.TRADE_SIZE} {symbol} at ${price:.2f}")
            else:
                messagebox.showerror("Error", "Insufficient position")
        else:
            messagebox.showerror("Error", "No price data available")

def main():
    root = tk.Tk()
    app = TradingDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main() 