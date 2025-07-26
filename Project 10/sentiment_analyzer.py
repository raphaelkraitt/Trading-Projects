import pandas as pd
from textblob import TextBlob
import config

def analyze_sentiment(text):
    """Analyze sentiment of text using TextBlob"""
    try:
        blob = TextBlob(str(text))
        return blob.sentiment.polarity
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return 0.0

def add_sentiment_to_news(news_df):
    """Add sentiment scores to news dataframe"""
    if news_df.empty:
        return news_df
    
    df = news_df.copy()
    
    # Analyze sentiment for titles and descriptions
    df['title_sentiment'] = df['title'].apply(analyze_sentiment)
    df['description_sentiment'] = df['description'].apply(analyze_sentiment)
    
    # Calculate combined sentiment (weighted average)
    df['combined_sentiment'] = (df['title_sentiment'] * 0.7 + df['description_sentiment'] * 0.3)
    
    # Add sentiment category
    df['sentiment_category'] = df['combined_sentiment'].apply(
        lambda x: 'positive' if x > 0.1 else 'negative' if x < -0.1 else 'neutral'
    )
    
    return df

def get_sentiment_statistics(sentiment_df):
    """Get sentiment statistics from analyzed dataframe"""
    if sentiment_df.empty:
        return {}
    
    stats = {
        'total_articles': len(sentiment_df),
        'mean_sentiment': sentiment_df['combined_sentiment'].mean(),
        'positive_articles': len(sentiment_df[sentiment_df['combined_sentiment'] > 0.1]),
        'negative_articles': len(sentiment_df[sentiment_df['combined_sentiment'] < -0.1]),
        'neutral_articles': len(sentiment_df[(sentiment_df['combined_sentiment'] >= -0.1) & (sentiment_df['combined_sentiment'] <= 0.1)])
    }
    
    # Calculate percentages
    total = stats['total_articles']
    if total > 0:
        stats['positive_percentage'] = (stats['positive_articles'] / total) * 100
        stats['negative_percentage'] = (stats['negative_articles'] / total) * 100
        stats['neutral_percentage'] = (stats['neutral_articles'] / total) * 100
    
    return stats

if __name__ == "__main__":
    from news_fetcher import NewsFetcher
    
    fetcher = NewsFetcher()
    news_df = fetcher.fetch_news()
    
    if not news_df.empty:
        sentiment_df = add_sentiment_to_news(news_df)
        stats = get_sentiment_statistics(sentiment_df)
        
        print("Sentiment Analysis Results:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\nSample articles with sentiment:")
        print(sentiment_df[['title', 'combined_sentiment', 'sentiment_category']].head()) 