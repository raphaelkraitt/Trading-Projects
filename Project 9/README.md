# Tkinter Trading Dashboard

A desktop GUI application in Python using Tkinter that displays live crypto prices (BTC, ETH) fetched from Binance, shows portfolio PnL, visualizes recent trade history, and includes buttons to execute mock trades.

## 🚀 Features
- **Live Price Display**: Real-time BTC/USDT and ETH/USDT prices from Binance
- **Portfolio Management**: Track balance, positions, and total portfolio value
- **Mock Trading**: Execute simulated BUY/SELL trades with real-time prices
- **Trade History**: Visualize recent trades in a scrollable table
- **Auto-updating**: Prices and portfolio data update every 5 seconds
- **User-friendly Interface**: Clean, intuitive GUI layout

## 📋 Requirements
- Python 3.8+
- Tkinter (usually included with Python)
- See `requirements.txt` for additional dependencies

## 🛠️ Installation
1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration
Edit `config.py` to change:
- Trading symbols (BTC/USDT, ETH/USDT)
- Update interval (default: 5 seconds)
- Window size and portfolio settings

## 🎯 Usage
Run the main script:
```bash
python trading_dashboard.py
```

## 📊 Interface Features
- **Live Prices Section**: Shows current BTC and ETH prices
- **Portfolio Section**: Displays current balance and total portfolio value
- **Mock Trading Section**: Dropdown to select symbol, BUY/SELL buttons
- **Trade History Section**: Table showing recent trades with timestamps

## 📝 Example Usage
1. Launch the application
2. Watch live prices update automatically
3. Select a symbol (BTC/USDT or ETH/USDT) from the dropdown
4. Click BUY to simulate buying crypto
5. Click SELL to simulate selling crypto
6. View trade history in the table
7. Monitor portfolio value changes

## 📁 Project Structure
```
Project 9/
├── config.py              # Configuration settings
├── data_fetcher.py        # Live price fetching from Binance
├── portfolio.py           # Portfolio management and PnL calculation
├── trading_dashboard.py   # Main Tkinter GUI application
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── charts/                # Output charts (if any)
```

## ⚠️ Notes
- This application is for **simulation and educational purposes only**. It does not place real trades.
- The application uses public Binance API endpoints and may be rate-limited.
- All trades are simulated and do not affect real money or positions.
- The GUI updates automatically every 5 seconds (configurable).

## 🤝 Contributing
- Pull requests and improvements are welcome!

## 📄 License
- For educational use only. No warranty or financial advice. 