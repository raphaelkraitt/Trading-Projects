# Portfolio Rebalancer for Stocks (MT5)

A Python application that connects to MetaTrader5, retrieves current holdings and prices for a portfolio of stocks, calculates an optimal rebalancing strategy using mean-variance optimization, and outputs suggested trades with a visual portfolio allocation pie chart.

## 🚀 Features
- Connects to MetaTrader5 (MT5) for real portfolio and price data
- Retrieves current holdings and latest prices for a configurable stock portfolio
- Performs mean-variance optimization to find optimal weights
- Calculates suggested trades to rebalance portfolio
- Plots portfolio allocation as a pie chart
- All charts saved in the `charts/` directory

## 📋 Requirements
- Python 3.8+
- MetaTrader5 (MT5) installed on your system
- MT5 account (demo or real, optional for login)
- See `requirements.txt` for Python dependencies

## 🛠️ Installation
1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **(Optional) Set up `.env` for MT5 login**:
   - Copy `env_example.txt` to `.env` and fill in your MT5 credentials if needed

## ⚙️ Configuration
Edit `config.py` to change:
- Portfolio symbols and target weights
- Optimization and chart settings

## 🎯 Usage
Run the main script:
```bash
python main.py
```

## 📊 Output
- **Suggested Trades**: Shares to buy/sell for rebalancing
- **Portfolio Allocation Chart**: Pie chart of optimal weights
- All charts are saved in the `charts/` directory

## 📝 Example Output
```
=== Portfolio Rebalancer for Stocks (MT5) ===
Current Holdings: {'AAPL': 10, 'MSFT': 5, ...}
Latest Prices: {'AAPL': 170.25, 'MSFT': 320.10, ...}
Optimal Weights: {'AAPL': 0.18, 'MSFT': 0.22, ...}
Total Portfolio Value: $12345.67

Suggested Trades (positive: buy, negative: sell):
  AAPL: +2.15 shares
  MSFT: -1.05 shares
  ...

Saved portfolio allocation chart: charts/portfolio_allocation.png
Done.
```

## 📁 Project Structure
```
Project 7/
├── config.py             # Configuration
├── mt5_portfolio.py      # MT5 connection and data fetching
├── optimizer.py          # Mean-variance optimization
├── rebalancer.py         # Rebalancing logic
├── chart_generator.py    # Pie chart plotting
├── main.py               # Main script
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── charts/               # Output charts (created automatically)
```

## ⚠️ Notes
- This bot is for **simulation and educational purposes only**. It does not place real trades.
- You must have MetaTrader5 installed and running on your system for data fetching.
- The optimization uses historical daily data for 1 year by default (configurable).

## 🤝 Contributing
- Pull requests and improvements are welcome!

## 📄 License
- For educational use only. No warranty or financial advice. 