import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from textblob import TextBlob
from typing import List, Dict, Tuple
import config

class SentimentAnalyzer:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained sentiment analysis model"""
        try:
            print(f"Loading sentiment model: {config.SENTIMENT_MODEL}")
            self.tokenizer = AutoTokenizer.from_pretrained(config.SENTIMENT_MODEL)
            self.model = AutoModelForSequenceClassification.from_pretrained(config.SENTIMENT_MODEL)
            self.model.eval()
            print("Sentiment model loaded successfully")
        except Exception as e:
            print(f"Failed to load sentiment model: {e}")
            print("Falling back to TextBlob for sentiment analysis")
            self.model = None
            self.tokenizer = None
    
    def analyze_text_transformer(self, text: str) -> float:
        """Analyze sentiment using transformer model"""
        if not self.model or not self.tokenizer:
            return self.analyze_text_textblob(text)
        
        try:
            # Tokenize and truncate text
            inputs = self.tokenizer(
                text, 
                truncation=True, 
                padding=True, 
                max_length=config.MAX_TEXT_LENGTH,
                return_tensors="pt"
            )
            
            # Get model prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=1)
            
            # Map to sentiment score (-1 to 1)
            # Assuming model outputs: [negative, neutral, positive]
            if probabilities.shape[1] == 3:
                # Convert to -1 to 1 scale
                sentiment_score = (probabilities[0][2] - probabilities[0][0]).item()
            else:
                # Binary classification
                sentiment_score = (probabilities[0][1] - 0.5) * 2
            
            return sentiment_score
            
        except Exception as e:
            print(f"Error in transformer analysis: {e}")
            return self.analyze_text_textblob(text)
    
    def analyze_text_textblob(self, text: str) -> float:
        """Analyze sentiment using TextBlob as fallback"""
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity
        except Exception as e:
            print(f"Error in TextBlob analysis: {e}")
            return 0.0
    
    def analyze_text(self, text: str) -> float:
        """Analyze sentiment of text using best available method"""
        if self.model:
            return self.analyze_text_transformer(text)
        else:
            return self.analyze_text_textblob(text)
    
    def analyze_batch(self, texts: List[str]) -> List[float]:
        """Analyze sentiment for a batch of texts"""
        sentiments = []
        for text in texts:
            sentiment = self.analyze_text(text)
            sentiments.append(sentiment)
        return sentiments
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = 'text') -> pd.DataFrame:
        """Analyze sentiment for all texts in a dataframe"""
        if df.empty:
            return df
        
        # Create a copy to avoid modifying original
        result_df = df.copy()
        
        # Analyze sentiment for each text
        sentiments = []
        for text in result_df[text_column]:
            sentiment = self.analyze_text(str(text))
            sentiments.append(sentiment)
        
        result_df['sentiment_score'] = sentiments
        
        # Add sentiment category
        result_df['sentiment_category'] = result_df['sentiment_score'].apply(
            lambda x: 'positive' if x > 0.1 else 'negative' if x < -0.1 else 'neutral'
        )
        
        return result_df
    
    def get_sentiment_statistics(self, df: pd.DataFrame) -> Dict:
        """Get sentiment statistics from analyzed dataframe"""
        if df.empty or 'sentiment_score' not in df.columns:
            return {}
        
        stats = {
            'total_posts': len(df),
            'mean_sentiment': df['sentiment_score'].mean(),
            'median_sentiment': df['sentiment_score'].median(),
            'std_sentiment': df['sentiment_score'].std(),
            'positive_count': len(df[df['sentiment_score'] > 0.1]),
            'negative_count': len(df[df['sentiment_score'] < -0.1]),
            'neutral_count': len(df[(df['sentiment_score'] >= -0.1) & (df['sentiment_score'] <= 0.1)]),
            'min_sentiment': df['sentiment_score'].min(),
            'max_sentiment': df['sentiment_score'].max()
        }
        
        # Calculate percentages
        total = stats['total_posts']
        if total > 0:
            stats['positive_percentage'] = (stats['positive_count'] / total) * 100
            stats['negative_percentage'] = (stats['negative_count'] / total) * 100
            stats['neutral_percentage'] = (stats['neutral_count'] / total) * 100
        
        return stats
    
    def get_aggregated_sentiment(self, df: pd.DataFrame, time_window: str = '1H') -> pd.DataFrame:
        """Get sentiment aggregated over time windows"""
        if df.empty or 'sentiment_score' not in df.columns:
            return pd.DataFrame()
        
        # Ensure datetime column exists
        if 'created_at' not in df.columns:
            return pd.DataFrame()
        
        # Convert to datetime if needed
        df_copy = df.copy()
        df_copy['created_at'] = pd.to_datetime(df_copy['created_at'])
        
        # Set as index for resampling
        df_copy.set_index('created_at', inplace=True)
        
        # Aggregate sentiment over time windows
        aggregated = df_copy['sentiment_score'].resample(time_window).agg([
            'mean', 'std', 'count'
        ]).fillna(0)
        
        aggregated.columns = ['sentiment_mean', 'sentiment_std', 'post_count']
        
        return aggregated.reset_index()

if __name__ == "__main__":
    # Test the sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    # Test texts
    test_texts = [
        "Bitcoin is going to the moon! 🚀",
        "I'm worried about the crypto market crash",
        "Bitcoin price is stable today",
        "This is the worst investment ever",
        "Amazing gains on my crypto portfolio!"
    ]
    
    print("Testing sentiment analysis:")
    for text in test_texts:
        sentiment = analyzer.analyze_text(text)
        print(f"Text: {text}")
        print(f"Sentiment: {sentiment:.3f}")
        print("-" * 50) 