# Crypto Sentiment Analysis Bot

A Python-based trading bot that analyzes sentiment from Twitter and Reddit posts about Bitcoin and cryptocurrencies, then generates buy/sell trading signals based on sentiment scores.

## 🚀 Features

- **Multi-Source Data Collection**: Scrapes tweets and Reddit posts about Bitcoin/crypto
- **Advanced Sentiment Analysis**: Uses pre-trained transformer models (HuggingFace) for accurate sentiment scoring
- **Trading Signal Generation**: Generates BUY/SELL signals based on configurable sentiment thresholds
- **Comprehensive Visualization**: Creates detailed charts and dashboards for sentiment analysis
- **Real-time Monitoring**: Supports continuous monitoring with periodic analysis
- **Performance Tracking**: Tracks trading decisions and performance metrics

## 📋 Requirements

- Python 3.8+
- Twitter API credentials (optional)
- Reddit API credentials (optional)
- Internet connection for data collection

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API credentials** (optional):
   Create a `.env` file in the project directory with your API credentials:
   ```
   # Twitter API (optional)
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET=your_twitter_api_secret
   TWITTER_ACCESS_TOKEN=your_twitter_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   TWITTER_BEARER_TOKEN=your_twitter_bearer_token
   
   # Reddit API (optional)
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   ```

## 🎯 Usage

### Basic Usage

Run a single analysis cycle:
```bash
python main.py
```

### Advanced Usage

**Demo Mode** (uses sample data, no API required):
```bash
python main.py --mode demo
```

**Single Analysis** with custom parameters:
```bash
python main.py --mode single --hours 12 --no-charts
```

**Continuous Monitoring**:
```bash
python main.py --mode continuous --interval 30 --max-cycles 10
```

### Command Line Options

- `--mode`: Operation mode (`single`, `continuous`, `demo`)
- `--hours`: Hours of data to analyze (default: 24)
- `--interval`: Interval between analyses in minutes (continuous mode, default: 60)
- `--max-cycles`: Maximum number of cycles (continuous mode)
- `--no-charts`: Disable chart saving

## 📊 Output

The bot generates several types of visualizations:

1. **Sentiment Distribution**: Histogram and box plots of sentiment scores
2. **Sentiment Over Time**: Time series analysis of sentiment trends
3. **Sentiment Categories**: Pie charts showing positive/negative/neutral breakdown
4. **Trading Signals**: Visualization of BUY/SELL signals over time
5. **Comprehensive Dashboard**: All-in-one analysis summary

Charts are saved in the `sentiment_charts/` directory.

## 🔧 Configuration

Edit `config.py` to customize:

- **Trading Thresholds**: Adjust buy/sell sentiment thresholds
- **Data Collection**: Modify query keywords and limits
- **Model Settings**: Change sentiment analysis model
- **Visualization**: Customize chart settings

### Key Configuration Parameters

```python
# Trading thresholds
SENTIMENT_THRESHOLD_BUY = 0.3    # Generate BUY signal above this
SENTIMENT_THRESHOLD_SELL = -0.3  # Generate SELL signal below this

# Data collection
QUERY_KEYWORDS = ['bitcoin', 'btc', 'crypto', 'cryptocurrency']
MAX_TWEETS_PER_QUERY = 100
MAX_REDDIT_POSTS_PER_QUERY = 50

# Model settings
SENTIMENT_MODEL = 'cardiffnlp/twitter-roberta-base-sentiment-latest'
```

## 📁 Project Structure

```
Project 2/
├── main.py                 # Main bot script
├── config.py              # Configuration settings
├── data_collector.py      # Twitter/Reddit data collection
├── sentiment_analyzer.py  # Sentiment analysis engine
├── trading_signals.py     # Trading signal generation
├── visualizer.py          # Chart generation
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── sentiment_charts/     # Generated charts (created automatically)
```

## 🧠 How It Works

1. **Data Collection**: Scrapes recent tweets and Reddit posts about Bitcoin/crypto
2. **Sentiment Analysis**: Analyzes text sentiment using transformer models
3. **Signal Generation**: Calculates weighted sentiment scores and generates trading signals
4. **Visualization**: Creates comprehensive charts and dashboards
5. **Decision Making**: Provides trading recommendations with confidence scores

## 📈 Trading Logic

The bot uses a weighted sentiment scoring system:

- **Engagement Weighting**: Tweets with more retweets/likes get higher weight
- **Reddit Weighting**: Posts with higher scores and upvote ratios get higher weight
- **Threshold-Based Signals**: BUY when sentiment > 0.3, SELL when sentiment < -0.3
- **Cooldown Period**: Prevents signal spam with configurable cooldown

## ⚠️ Important Notes

- **API Limits**: Twitter and Reddit have rate limits. The bot handles these automatically.
- **Demo Mode**: Use demo mode if you don't have API credentials.
- **Simulation Only**: This bot generates signals but doesn't execute real trades.
- **Data Quality**: Sentiment analysis accuracy depends on the quality of collected data.

## 🔍 Troubleshooting

**No data collected**:
- Check API credentials in `.env` file
- Verify internet connection
- Try demo mode first

**Model loading errors**:
- Ensure you have sufficient disk space for model downloads
- Check internet connection for model downloads
- The bot will fall back to TextBlob if transformer models fail

**Chart generation errors**:
- Ensure matplotlib and seaborn are installed
- Check write permissions for the charts directory

## 📝 Example Output

```
🚀 Crypto Sentiment Analysis Bot
==================================================
🔄 Starting Analysis Cycle - 2024-01-15 14:30:00
==================================================

📊 Collecting data from the last 24 hours...
📈 Collected 150 posts/tweets

🧠 Performing sentiment analysis...
📊 Sentiment Analysis Results:
   Mean Sentiment: 0.245
   Positive Posts: 85 (56.7%)
   Negative Posts: 35 (23.3%)
   Neutral Posts: 30 (20.0%)

💰 Generating trading decision...
📈 Trading Decision: HOLD
   Confidence: 0.45
   Sentiment Score: 0.245
   Reason: Sentiment-based HOLD signal with 0.45 confidence

📊 Creating visualizations...
   📈 Sentiment distribution chart: sentiment_distribution_20240115_143000.png
   📈 Sentiment over time chart: sentiment_over_time_20240115_143000.png
   📈 Sentiment categories chart: sentiment_categories_20240115_143000.png
   📈 Comprehensive analysis dashboard: comprehensive_analysis_20240115_143000.png
✅ Created 4 charts

✅ Analysis cycle completed successfully!
   Data points analyzed: 150
   Charts created: 4
   Trading decision: HOLD
```

## 🤝 Contributing

Feel free to contribute by:
- Adding new data sources
- Improving sentiment analysis models
- Enhancing visualization features
- Optimizing trading algorithms

## 📄 License

This project is for educational purposes. Use at your own risk for actual trading.

## ⚡ Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Run demo: `python main.py --mode demo`
3. Check generated charts in `sentiment_charts/` directory

The bot is ready to use! 🚀 