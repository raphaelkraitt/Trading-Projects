# News Sentiment Bot for Stock Trading (TSLA)

A Python bot that fetches recent financial news headlines about Tesla (TSLA) from a news API, performs sentiment analysis using TextBlob, and uses sentiment scores to simulate buy/sell decisions in MT5. Visualizes headline sentiment trends with charts.

## 🚀 Features
- **News Fetching**: Retrieves recent Tesla news from NewsAPI
- **Sentiment Analysis**: Uses TextBlob to analyze article sentiment
- **MT5 Integration**: Connects to MetaTrader5 for price data and trading simulation
- **Trading Signals**: Generates BUY/SELL signals based on sentiment thresholds
- **Visualization**: Plots sentiment trends and trade signals
- **Simulated Trading**: Executes mock trades based on sentiment analysis

## 📋 Requirements
- Python 3.8+
- MetaTrader5 (MT5) installed (optional)
- NewsAPI key (optional, uses demo mode if not provided)
- See `requirements.txt` for Python dependencies

## 🛠️ Installation
1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **(Optional) Set up API keys**:
   - Copy `env_example.txt` to `.env`
   - Add your NewsAPI key and MT5 credentials

## ⚙️ Configuration
Edit `config.py` to change:
- News query and API settings
- Sentiment thresholds for trading signals
- MT5 connection and trading parameters
- Chart output directory

## 🎯 Usage
Run the main script:
```bash
python main.py
```

## 📊 Output
- **Sentiment Trends Chart**: Shows sentiment scores over time with thresholds
- **Trade Signals Chart**: Displays sentiment with BUY/SELL signals
- **Sentiment Statistics**: Article counts and sentiment distribution
- **Trading Decisions**: Simulated BUY/SELL orders based on sentiment

## 📝 Example Output
```
=== News Sentiment Bot for Stock Trading (TSLA) ===

📰 Fetching Tesla news...
✅ Fetched 20 articles

🧠 Analyzing sentiment...
📊 Sentiment Analysis Results:
   Total Articles: 20
   Mean Sentiment: 0.245
   Positive: 12 (60.0%)
   Negative: 3 (15.0%)
   Neutral: 5 (25.0%)

📈 Connecting to MT5...
✅ Current TSLA price: $245.50

💰 Generating trading signals...
📊 Signal: BUY (Sentiment: 0.245)
✅ Simulated BUY order executed

📊 Creating charts...
   📈 Sentiment trends chart: charts/tesla_sentiment_trends.png
   📈 Trade signals chart: charts/tesla_trade_signals.png

📋 Summary:
   Articles analyzed: 20
   Average sentiment: 0.245
   Trading signal: BUY
   Trades executed: 1

✅ Analysis completed!
```

## 📁 Project Structure
```
Project 10/
├── config.py              # Configuration settings
├── news_fetcher.py        # Fetches news from NewsAPI
├── sentiment_analyzer.py  # TextBlob sentiment analysis
├── mt5_trader.py          # MT5 connection and trading logic
├── chart_generator.py     # Sentiment and trade visualization
├── main.py                # Main orchestration script
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── charts/                # Output charts (created automatically)
```

## ⚠️ Notes
- This bot is for **simulation and educational purposes only**. It does not place real trades.
- NewsAPI has rate limits. The bot uses demo mode if no API key is provided.
- MT5 connection is optional. The bot will use simulated price data if MT5 is not available.
- Sentiment analysis is simplified and should not be used as the sole basis for real trading decisions.

## 🤝 Contributing
- Pull requests and improvements are welcome!

## 📄 License
- For educational use only. No warranty or financial advice. 