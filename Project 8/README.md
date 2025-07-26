# Backtesting Framework for Crypto Strategies (BTC/USDT)

A simple Python backtesting engine that simulates trading strategies (e.g., SMA crossover) on historical Binance BTC/USDT data, calculates performance metrics (total return, max drawdown, Sharpe ratio), and produces equity curve plots saved as images.

## 🚀 Features
- Fetches historical BTC/USDT OHLCV data from Binance (via ccxt)
- Implements SMA crossover strategy (configurable)
- Simulates trades, tracks balance and equity
- Calculates total return, max drawdown, and Sharpe ratio
- Plots equity curve and saves as image
- All charts saved in the `charts/` directory

## 📋 Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## 🛠️ Installation
1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration
Edit `config.py` to change:
- Symbol, timeframe, and data settings
- SMA strategy parameters
- Backtest and chart settings

## 🎯 Usage
Run the main script:
```bash
python main.py
```

## 📊 Output
- **Equity Curve Chart**: Simulated account equity over time
- **Performance Metrics**: Total return, max drawdown, Sharpe ratio
- **Trade Log**: Details of each trade
- All charts are saved in the `charts/` directory

## 📝 Example Output
```
=== Crypto Backtesting Framework (BTC/USDT) ===
Loaded 2000 bars of BTC/USDT data.
SMA signals calculated.
Simulated 12 trades.

Performance Metrics:
  Total Return: 18.45%
  Max Drawdown: 7.23%
  Sharpe Ratio: 1.45

Saved equity curve chart: charts/backtest_equity_curve.png

Trade Log:
              datetime action      price      balance
1995 2024-05-31 10:00:00   BUY  67000.00  9330.00
1998 2024-05-31 13:00:00  SELL  67500.00 10055.00
...
Done.
```

## 📁 Project Structure
```
Project 8/
├── config.py           # Configuration
├── data_fetcher.py     # Fetches and caches OHLCV data
├── strategy.py         # SMA crossover strategy
├── backtester.py       # Backtesting engine and metrics
├── chart_generator.py  # Equity curve plotting
├── main.py             # Main script
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── charts/             # Output charts (created automatically)
```

## ⚠️ Notes
- This bot is for **simulation and educational purposes only**. It does not place real trades.
- The SMA crossover strategy is simple and can be replaced with more advanced strategies.

## 🤝 Contributing
- Pull requests and improvements are welcome!

## 📄 License
- For educational use only. No warranty or financial advice. 