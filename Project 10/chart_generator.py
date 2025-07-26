import matplotlib.pyplot as plt
import pandas as pd
import os
import config

def plot_sentiment_trends(sentiment_df, save=True):
    """Plot sentiment trends over time"""
    if sentiment_df.empty:
        return ""
    
    # Convert published_at to datetime
    df = sentiment_df.copy()
    df['published_at'] = pd.to_datetime(df['published_at'])
    df = df.sort_values('published_at')
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Sentiment over time
    ax1.plot(df['published_at'], df['combined_sentiment'], marker='o', linewidth=2, markersize=4)
    ax1.axhline(y=config.SENTIMENT_THRESHOLD_BUY, color='green', linestyle='--', 
               label=f'Buy Threshold ({config.SENTIMENT_THRESHOLD_BUY})')
    ax1.axhline(y=config.SENTIMENT_THRESHOLD_SELL, color='red', linestyle='--', 
               label=f'Sell Threshold ({config.SENTIMENT_THRESHOLD_SELL})')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax1.set_ylabel('Sentiment Score')
    ax1.set_title('Tesla News Sentiment Trends')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Sentiment distribution
    sentiment_counts = df['sentiment_category'].value_counts()
    colors = ['lightgreen', 'lightcoral', 'lightblue']
    ax2.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', colors=colors)
    ax2.set_title('Sentiment Distribution')
    
    plt.tight_layout()
    
    if save:
        if not os.path.exists(config.CHART_SAVE_PATH):
            os.makedirs(config.CHART_SAVE_PATH)
        filename = f"tesla_sentiment_trends.{config.CHART_FORMAT}"
        filepath = os.path.join(config.CHART_SAVE_PATH, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        return filepath
    else:
        plt.show()
        return ""

def plot_trade_signals(trade_df, sentiment_df, save=True):
    """Plot trade signals with sentiment context"""
    if trade_df.empty or sentiment_df.empty:
        return ""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Sentiment with trade signals
    sentiment_df['published_at'] = pd.to_datetime(sentiment_df['published_at'])
    ax1.plot(sentiment_df['published_at'], sentiment_df['combined_sentiment'], 
            marker='o', linewidth=2, markersize=4, label='Sentiment Score')
    
    # Mark trade signals
    trade_df['timestamp'] = pd.to_datetime(trade_df['timestamp'])
    buy_trades = trade_df[trade_df['signal'] == 'BUY']
    sell_trades = trade_df[trade_df['signal'] == 'SELL']
    
    if not buy_trades.empty:
        ax1.scatter(buy_trades['timestamp'], buy_trades['sentiment_score'], 
                   color='green', s=100, marker='^', label='BUY Signal', zorder=5)
    if not sell_trades.empty:
        ax1.scatter(sell_trades['timestamp'], sell_trades['sentiment_score'], 
                   color='red', s=100, marker='v', label='SELL Signal', zorder=5)
    
    ax1.axhline(y=config.SENTIMENT_THRESHOLD_BUY, color='green', linestyle='--', 
               label=f'Buy Threshold ({config.SENTIMENT_THRESHOLD_BUY})')
    ax1.axhline(y=config.SENTIMENT_THRESHOLD_SELL, color='red', linestyle='--', 
               label=f'Sell Threshold ({config.SENTIMENT_THRESHOLD_SELL})')
    ax1.set_ylabel('Sentiment Score')
    ax1.set_title('Sentiment with Trade Signals')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Trade frequency
    if not trade_df.empty:
        trade_counts = trade_df['signal'].value_counts()
        ax2.bar(trade_counts.index, trade_counts.values, color=['green', 'red'])
        ax2.set_title('Trade Signal Distribution')
        ax2.set_ylabel('Number of Trades')
    
    plt.tight_layout()
    
    if save:
        if not os.path.exists(config.CHART_SAVE_PATH):
            os.makedirs(config.CHART_SAVE_PATH)
        filename = f"tesla_trade_signals.{config.CHART_FORMAT}"
        filepath = os.path.join(config.CHART_SAVE_PATH, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        return filepath
    else:
        plt.show()
        return ""

if __name__ == "__main__":
    from news_fetcher import NewsFetcher
    from sentiment_analyzer import add_sentiment_to_news
    
    fetcher = NewsFetcher()
    news_df = fetcher.fetch_news()
    
    if not news_df.empty:
        sentiment_df = add_sentiment_to_news(news_df)
        print(plot_sentiment_trends(sentiment_df, save=False)) 