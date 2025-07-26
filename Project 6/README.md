# Arbitrage Bot between Binance and MEXC (BTC/USDT)

A Python bot that fetches real-time BTC/USDT prices from Binance and MEXC, detects arbitrage opportunities by comparing prices and accounting for fees, and simulates placing buy and sell orders accordingly. Outputs arbitrage signals and a profit/loss chart.

## 🚀 Features
- Fetches real-time BTC/USDT prices from Binance and MEXC (via ccxt)
- Detects arbitrage opportunities (after fees)
- Simulates buy/sell orders and tracks balance
- Outputs arbitrage signals and trade log
- Plots simulated profit/loss (equity curve)
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
- Symbol, trade amount, fees, minimum profit
- Chart output directory

## 🎯 Usage
Run the main script:
```bash
python main.py
```

## 📊 Output
- **Equity Curve Chart**: Simulated profit/loss over time
- **Trade Log**: Details of each arbitrage trade
- All charts are saved in the `charts/` directory

## 📝 Example Output
```
=== Arbitrage Bot: Binance vs MEXC ===
Cycle 1/30
No arbitrage opportunity. Balance: 10000.00
...
Cycle 7/30
Arbitrage: BINANCE->MEXC | Profit: 2.15 USDT | New Balance: 10002.15
...
Saved equity curve chart: charts/arbitrage_equity_curve.png

Trade Log:
             timestamp       direction  profit    balance
6 2024-06-01 15:30:00  BINANCE->MEXC    2.15  10002.15
...
Done.
```

## 📁 Project Structure
```
Project 6/
├── config.py           # Configuration
├── arbitrage_bot.py    # Arbitrage logic and simulation
├── main.py             # Main script
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── charts/             # Output charts (created automatically)
```

## ⚠️ Notes
- This bot is for **simulation and educational purposes only**. It does not place real trades.
- The bot uses public endpoints and may be rate-limited by the exchanges.
- You can adjust the number of cycles and interval in `main.py` for longer/shorter simulations.

## 🤝 Contributing
- Pull requests and improvements are welcome!

## 📄 License
- For educational use only. No warranty or financial advice. 