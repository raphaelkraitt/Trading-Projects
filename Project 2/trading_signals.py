import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import config

class TradingSignals:
    def __init__(self):
        self.last_signal_time = None
        self.signal_history = []
    
    def generate_signal(self, sentiment_score: float, sentiment_stats: Dict = None) -> Optional[str]:
        """Generate trading signal based on sentiment score"""
        current_time = datetime.now()
        
        # Check cooldown period
        if self.last_signal_time:
            time_since_last = current_time - self.last_signal_time
            if time_since_last < timedelta(hours=config.SIGNAL_COOLDOWN_HOURS):
                return None
        
        # Generate signal based on sentiment thresholds
        signal = None
        if sentiment_score >= config.SENTIMENT_THRESHOLD_BUY:
            signal = "BUY"
        elif sentiment_score <= config.SENTIMENT_THRESHOLD_SELL:
            signal = "SELL"
        
        # Record signal if generated
        if signal:
            self.last_signal_time = current_time
            signal_data = {
                'timestamp': current_time,
                'signal': signal,
                'sentiment_score': sentiment_score,
                'sentiment_stats': sentiment_stats
            }
            self.signal_history.append(signal_data)
            
            print(f"Generated {signal} signal with sentiment score: {sentiment_score:.3f}")
        
        return signal
    
    def generate_signal_from_dataframe(self, df: pd.DataFrame) -> Optional[str]:
        """Generate trading signal from analyzed dataframe"""
        if df.empty or 'sentiment_score' not in df.columns:
            return None
        
        # Calculate weighted average sentiment
        # Weight by engagement (retweets, likes, upvotes)
        weights = []
        for _, row in df.iterrows():
            if row['source'] == 'twitter':
                weight = (row.get('retweet_count', 0) + row.get('favorite_count', 0) + 1)
            elif row['source'] == 'reddit':
                weight = (row.get('score', 0) + 1) * row.get('upvote_ratio', 0.5)
            else:
                weight = 1
            weights.append(weight)
        
        # Calculate weighted average sentiment
        weighted_sentiment = np.average(df['sentiment_score'], weights=weights)
        
        # Get sentiment statistics
        sentiment_stats = {
            'weighted_sentiment': weighted_sentiment,
            'mean_sentiment': df['sentiment_score'].mean(),
            'total_posts': len(df),
            'positive_posts': len(df[df['sentiment_score'] > 0.1]),
            'negative_posts': len(df[df['sentiment_score'] < -0.1])
        }
        
        return self.generate_signal(weighted_sentiment, sentiment_stats)
    
    def get_signal_strength(self, sentiment_score: float) -> float:
        """Calculate signal strength based on sentiment score"""
        if sentiment_score >= config.SENTIMENT_THRESHOLD_BUY:
            return min((sentiment_score - config.SENTIMENT_THRESHOLD_BUY) / (1 - config.SENTIMENT_THRESHOLD_BUY), 1.0)
        elif sentiment_score <= config.SENTIMENT_THRESHOLD_SELL:
            return min((config.SENTIMENT_THRESHOLD_SELL - sentiment_score) / (config.SENTIMENT_THRESHOLD_SELL + 1), 1.0)
        else:
            return 0.0
    
    def get_signal_history(self) -> pd.DataFrame:
        """Get signal history as dataframe"""
        if not self.signal_history:
            return pd.DataFrame()
        
        return pd.DataFrame(self.signal_history)
    
    def get_recent_signals(self, hours: int = 24) -> pd.DataFrame:
        """Get signals from the last N hours"""
        if not self.signal_history:
            return pd.DataFrame()
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_signals = [s for s in self.signal_history if s['timestamp'] >= cutoff_time]
        
        return pd.DataFrame(recent_signals)
    
    def get_signal_statistics(self, hours: int = 24) -> Dict:
        """Get statistics about recent signals"""
        recent_signals = self.get_recent_signals(hours)
        
        if recent_signals.empty:
            return {}
        
        stats = {
            'total_signals': len(recent_signals),
            'buy_signals': len(recent_signals[recent_signals['signal'] == 'BUY']),
            'sell_signals': len(recent_signals[recent_signals['signal'] == 'SELL']),
            'avg_sentiment_score': recent_signals['sentiment_score'].mean(),
            'last_signal': recent_signals['timestamp'].max(),
            'signal_frequency_hours': hours / len(recent_signals) if len(recent_signals) > 0 else 0
        }
        
        return stats
    
    def should_trade(self, sentiment_score: float, confidence_threshold: float = 0.5) -> Tuple[bool, str, float]:
        """Determine if we should trade based on sentiment and confidence"""
        signal = self.generate_signal(sentiment_score)
        strength = self.get_signal_strength(sentiment_score)
        
        should_trade = signal is not None and strength >= confidence_threshold
        
        return should_trade, signal, strength
    
    def reset_signals(self):
        """Reset signal history and cooldown"""
        self.last_signal_time = None
        self.signal_history = []

class SentimentTradingBot:
    def __init__(self):
        self.signals = TradingSignals()
        self.trade_history = []
    
    def process_sentiment_data(self, df: pd.DataFrame) -> Dict:
        """Process sentiment data and generate trading decision"""
        if df.empty:
            return {'action': 'HOLD', 'reason': 'No data available'}
        
        # Generate signal
        signal = self.signals.generate_signal_from_dataframe(df)
        
        if not signal:
            return {'action': 'HOLD', 'reason': 'No clear signal'}
        
        # Get sentiment statistics
        sentiment_stats = {
            'mean_sentiment': df['sentiment_score'].mean(),
            'total_posts': len(df),
            'positive_ratio': len(df[df['sentiment_score'] > 0.1]) / len(df),
            'negative_ratio': len(df[df['sentiment_score'] < -0.1]) / len(df)
        }
        
        # Calculate confidence
        confidence = self.signals.get_signal_strength(sentiment_stats['mean_sentiment'])
        
        # Record trade decision
        trade_decision = {
            'timestamp': datetime.now(),
            'action': signal,
            'confidence': confidence,
            'sentiment_score': sentiment_stats['mean_sentiment'],
            'total_posts': sentiment_stats['total_posts'],
            'positive_ratio': sentiment_stats['positive_ratio'],
            'negative_ratio': sentiment_stats['negative_ratio']
        }
        
        self.trade_history.append(trade_decision)
        
        return {
            'action': signal,
            'confidence': confidence,
            'sentiment_score': sentiment_stats['mean_sentiment'],
            'reason': f"Sentiment-based {signal} signal with {confidence:.2f} confidence"
        }
    
    def get_trade_history(self) -> pd.DataFrame:
        """Get trade history as dataframe"""
        if not self.trade_history:
            return pd.DataFrame()
        
        return pd.DataFrame(self.trade_history)
    
    def get_performance_metrics(self) -> Dict:
        """Calculate performance metrics"""
        if not self.trade_history:
            return {}
        
        df = pd.DataFrame(self.trade_history)
        
        metrics = {
            'total_trades': len(df),
            'buy_trades': len(df[df['action'] == 'BUY']),
            'sell_trades': len(df[df['action'] == 'SELL']),
            'avg_confidence': df['confidence'].mean(),
            'avg_sentiment': df['sentiment_score'].mean(),
            'last_trade': df['timestamp'].max() if not df.empty else None
        }
        
        return metrics

if __name__ == "__main__":
    # Test the trading signals
    signals = TradingSignals()
    
    # Test sentiment scores
    test_sentiments = [0.8, -0.6, 0.2, -0.9, 0.1]
    
    print("Testing trading signals:")
    for sentiment in test_sentiments:
        signal = signals.generate_signal(sentiment)
        strength = signals.get_signal_strength(sentiment)
        print(f"Sentiment: {sentiment:.2f} -> Signal: {signal}, Strength: {strength:.2f}")
    
    print("\nSignal history:")
    print(signals.get_signal_history()) 