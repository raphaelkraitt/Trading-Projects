# 🚀 Crypto Trading Bot

A comprehensive Python trading bot that connects to Binance and MEXC, fetches BTC/USDT data, calculates technical indicators, generates buy/sell signals, and creates professional charts.

## ✨ Features

- **Multi-Exchange Support**: Connect to Binance and MEXC simultaneously
- **Real-time Data**: Fetch 1-hour OHLCV data for BTC/USDT
- **Technical Indicators**: 
  - Simple Moving Averages (SMA 20, 50)
  - Exponential Moving Averages (EMA 12, 26)
  - Relative Strength Index (RSI)
  - Bollinger Bands
- **Signal Generation**: Buy/sell signals based on indicator crossovers
- **Chart Generation**: Professional charts with indicators saved as PNG
- **Signal Analysis**: Comprehensive signal summary and recommendations
- **Demo Mode**: Test the bot without API keys using realistic demo data

## 📋 Requirements

- Python 3.8+
- Internet connection for data fetching
- API keys for Binance and/or MEXC (optional for demo mode)

## 🛠️ Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd crypto-trading-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys (optional)**
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env and add your API keys
   # For demo mode, you can leave them empty
   ```

## 🚀 Usage

### Quick Start (Demo Mode)

Run the bot with demo data to see how it works:

```bash
python main.py --demo
```

### Full Mode (with API keys)

1. **Set up your API keys** in the `.env` file:
   ```
   BINANCE_API_KEY=your_binance_api_key
   BINANCE_SECRET=your_binance_secret
   MEXC_API_KEY=your_mexc_api_key
   MEXC_SECRET=your_mexc_secret
   ```

2. **Run the bot**:
   ```bash
   python main.py
   ```

### Programmatic Usage

```python
from trading_bot import TradingBot

# Initialize the bot
bot = TradingBot()

# Fetch data from exchanges
data = bot.fetch_data()

# Process data and calculate indicators
processed_data = bot.process_data()

# Generate charts
charts = bot.generate_charts()

# Get latest signals
signals = bot.get_latest_signals()

# Get signal summary
summary = bot.get_signal_summary()
```

## 📊 Output

The bot generates:

1. **Console Output**: Real-time analysis and signal information
2. **Charts**: Professional PNG charts saved in the `charts/` directory
3. **Signal Analysis**: Buy/sell recommendations with confidence levels

### Sample Output

```
🚀 Starting Trading Bot Analysis...
================================================================================

🔄 Fetching BTC/USDT data from exchanges...
✓ Binance initialized successfully
✓ MEXC initialized successfully
Fetching data from binance...
✓ Fetched 500 candles from binance
Fetching data from mexc...
✓ Fetched 500 candles from mexc

📊 Processing data and calculating indicators...
Processing binance data...
✓ Processed binance data
Processing mexc data...
✓ Processed mexc data

📈 Generating charts...
Creating chart for binance...
Chart saved: charts/binance_20241201_143022_btc_trading_chart.png
Creating chart for mexc...
Chart saved: charts/mexc_20241201_143023_btc_trading_chart.png
Creating comparison chart...
Comparison chart saved: charts/comparison_20241201_143024.png

================================================================================
📊 LATEST TRADING SIGNALS
================================================================================

🔸 BINANCE:
   Timestamp: 2024-12-01 14:30:00
   Current Price: $43,250.50
   Recommendation: BUY
   SMA Signal: 1
   EMA Signal: 1
   RSI Signal: 0
   BB Signal: 0
   Combined Signal: 0.5000

🔸 MEXC:
   Timestamp: 2024-12-01 14:30:00
   Current Price: $43,245.75
   Recommendation: HOLD
   SMA Signal: 0
   EMA Signal: 0
   RSI Signal: 0
   BB Signal: 0
   Combined Signal: 0.0000
```

## 📈 Technical Indicators

### Moving Averages
- **SMA 20**: Short-term trend indicator
- **SMA 50**: Long-term trend indicator
- **EMA 12**: Fast exponential moving average
- **EMA 26**: Slow exponential moving average

### Oscillators
- **RSI**: Relative Strength Index (14-period)
  - Oversold: < 30 (buy signal)
  - Overbought: > 70 (sell signal)

### Volatility
- **Bollinger Bands**: 20-period with 2 standard deviations
  - Upper band: Resistance level
  - Lower band: Support level

## 🎯 Signal Generation

The bot generates signals based on:

1. **SMA Crossover**: Short SMA crosses above/below long SMA
2. **EMA Crossover**: Fast EMA crosses above/below slow EMA
3. **RSI Levels**: Oversold/overbought conditions
4. **Bollinger Bands**: Price touching upper/lower bands
5. **Combined Signal**: Weighted average of all signals

## 📁 Project Structure

```
crypto-trading-bot/
├── main.py              # Main entry point
├── trading_bot.py       # Main trading bot class
├── data_fetcher.py      # Exchange data fetching
├── signal_generator.py  # Technical indicators and signals
├── chart_generator.py   # Chart creation and saving
├── indicators.py        # Technical indicator calculations
├── config.py           # Configuration settings
├── demo_data.py        # Demo data generation
├── requirements.txt    # Python dependencies
├── env_example.txt     # Environment variables template
├── README.md          # This file
└── charts/            # Generated charts (created automatically)
```

## ⚙️ Configuration

Edit `config.py` to customize:

- Trading pair (default: BTC/USDT)
- Timeframe (default: 1h)
- Data limit (default: 500 candles)
- Indicator periods
- Signal thresholds
- Chart settings

## 🔧 Troubleshooting

### Common Issues

1. **No data fetched**
   - Check internet connection
   - Verify API keys are correct
   - Ensure trading pair is available on exchanges

2. **Import errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **Chart generation fails**
   - Ensure matplotlib is installed
   - Check write permissions for charts directory

### Debug Mode

Run with verbose output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## ⚠️ Disclaimer

This trading bot is for educational and research purposes only. It is not financial advice. Always:

- Do your own research before making trading decisions
- Never invest more than you can afford to lose
- Consider consulting with a financial advisor
- Test thoroughly with demo accounts before live trading

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- New features
- Documentation improvements
- Performance optimizations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [CCXT](https://github.com/ccxt/ccxt) for exchange connectivity
- [Pandas](https://pandas.pydata.org/) for data manipulation
- [Matplotlib](https://matplotlib.org/) for chart generation
- [NumPy](https://numpy.org/) for numerical computations

---

**Happy Trading! 📈💰** 