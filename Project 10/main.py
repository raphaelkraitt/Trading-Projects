import config
from news_fetcher import NewsFetcher
from sentiment_analyzer import add_sentiment_to_news, get_sentiment_statistics
from mt5_trader import MT5Trader
from chart_generator import plot_sentiment_trends, plot_trade_signals

def main():
    print("\n=== News Sentiment Bot for Stock Trading (TSLA) ===\n")
    
    # Step 1: Fetch news
    print("📰 Fetching Tesla news...")
    news_fetcher = NewsFetcher()
    news_df = news_fetcher.fetch_news()
    
    if news_df.empty:
        print("❌ No news articles found. Exiting.")
        return
    
    print(f"✅ Fetched {len(news_df)} articles")
    
    # Step 2: Analyze sentiment
    print("\n🧠 Analyzing sentiment...")
    sentiment_df = add_sentiment_to_news(news_df)
    stats = get_sentiment_statistics(sentiment_df)
    
    print("📊 Sentiment Analysis Results:")
    print(f"   Total Articles: {stats.get('total_articles', 0)}")
    print(f"   Mean Sentiment: {stats.get('mean_sentiment', 0):.3f}")
    print(f"   Positive: {stats.get('positive_articles', 0)} ({stats.get('positive_percentage', 0):.1f}%)")
    print(f"   Negative: {stats.get('negative_articles', 0)} ({stats.get('negative_percentage', 0):.1f}%)")
    print(f"   Neutral: {stats.get('neutral_articles', 0)} ({stats.get('neutral_percentage', 0):.1f}%)")
    
    # Step 3: Connect to MT5 and generate trading signals
    print("\n📈 Connecting to MT5...")
    trader = MT5Trader()
    
    if not trader.connected:
        print("⚠️ MT5 not connected. Using simulated price data.")
        current_price = 250.0  # Simulated TSLA price
    else:
        current_price = trader.get_current_price()
        if current_price:
            print(f"✅ Current TSLA price: ${current_price:.2f}")
        else:
            print("⚠️ Could not get current price. Using simulated data.")
            current_price = 250.0
    
    # Step 4: Generate trading signals based on sentiment
    print("\n💰 Generating trading signals...")
    mean_sentiment = stats.get('mean_sentiment', 0)
    signal = trader.generate_signal(mean_sentiment)
    
    if signal:
        print(f"📊 Signal: {signal} (Sentiment: {mean_sentiment:.3f})")
        trade = trader.simulate_trade(signal, mean_sentiment, current_price)
        if trade:
            print(f"✅ Simulated {signal} order executed")
    else:
        print(f"📊 No signal generated (Sentiment: {mean_sentiment:.3f})")
    
    # Step 5: Create visualizations
    print("\n📊 Creating charts...")
    sentiment_chart = plot_sentiment_trends(sentiment_df, save=True)
    if sentiment_chart:
        print(f"   📈 Sentiment trends chart: {sentiment_chart}")
    
    trade_df = trader.get_trade_history()
    if not trade_df.empty:
        trade_chart = plot_trade_signals(trade_df, sentiment_df, save=True)
        if trade_chart:
            print(f"   📈 Trade signals chart: {trade_chart}")
    
    # Step 6: Print summary
    print("\n📋 Summary:")
    print(f"   Articles analyzed: {len(sentiment_df)}")
    print(f"   Average sentiment: {mean_sentiment:.3f}")
    print(f"   Trading signal: {signal or 'HOLD'}")
    print(f"   Trades executed: {len(trade_df)}")
    
    # Cleanup
    trader.shutdown()
    print("\n✅ Analysis completed!")

if __name__ == "__main__":
    main() 