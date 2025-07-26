# Stock Momentum Trading Bot with MT5

A Python bot that connects to MetaTrader5, fetches hourly price data for AAPL stock, calculates momentum indicators (RSI, MACD), simulates buy/sell orders based on RSI thresholds, and plots price with RSI and MACD overlays, saving screenshots.

## 🚀 Features
- Connects to MetaTrader5 (MT5) for real market data
- Fetches hourly OHLCV data for AAPL (configurable)
- Calculates RSI and MACD using the `ta` library
- Simulates trading based on RSI overbought/oversold signals
- Tracks simulated balance, positions, and equity curve
- Plots price, RSI, MACD, and trade signals
- Saves all charts to the `charts/` directory

## 📋 Requirements
- Python 3.8+
- MetaTrader5 (MT5) installed on your system
- MT5 terminal path (optional, for custom installations)
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
- Trading symbol (default: AAPL)
- Timeframe (default: H1)
- RSI/MACD parameters
- Trade size, initial balance
- Chart output directory

## 🎯 Usage
Run the main script:
```bash
python main.py
```

## 📊 Output
- **Price/RSI/MACD Chart**: Shows price, RSI, MACD, and buy/sell signals
- **Equity Curve Chart**: Shows simulated account equity over time
- All charts are saved in the `charts/` directory

## 📝 Example Output
```
=== Stock Momentum Trading Bot with MT5 ===
Fetched 500 bars of AAPL data.
Indicators calculated.
Simulated 7 trades.
Saved price/indicator chart: AAPL_momentum_chart_20240601_153000.png
Saved equity curve chart: equity_curve_20240601_153000.png

Trade Log:
              datetime action       price        rsi  position      balance
495 2024-05-31 10:00:00   BUY  170.250000  28.123456        10  9830.00
498 2024-05-31 13:00:00  SELL  172.500000  71.234567         0 10055.00

Done.
```

## 📁 Project Structure
```
Project 3/
├── main.py            # Main script
├── config.py          # Configuration
├── data_fetcher.py    # MT5 data fetching
├── indicators.py      # RSI/MACD calculation
├── trading_bot.py     # Simulated trading logic
├── chart_generator.py # Chart plotting
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── charts/            # Output charts (created automatically)
```

## ⚠️ Notes
- This bot is for **simulation and educational purposes only**. It does not place real trades.
- You must have MetaTrader5 installed and running on your system for data fetching.
- If you do not provide MT5 login details, the bot will use the default terminal connection (if available).
- The bot uses simple RSI-based logic for demonstration. You can expand it with more advanced strategies.

## 🤝 Contributing
- Pull requests and improvements are welcome!

## 📄 License
- For educational use only. No warranty or financial advice. 