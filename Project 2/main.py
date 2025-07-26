#!/usr/bin/env python3
"""
Crypto Sentiment Analysis Bot
=============================

This bot scrapes recent tweets and Reddit posts about Bitcoin/crypto,
performs sentiment analysis using a pre-trained transformer model,
and generates buy/sell trading signals based on sentiment scores.

Features:
- Data collection from Twitter and Reddit
- Sentiment analysis using HuggingFace transformers
- Trading signal generation with configurable thresholds
- Comprehensive visualization and chart generation
- Simulated trading with performance tracking
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
import sys

# Import our modules
from data_collector import DataCollector
from sentiment_analyzer import SentimentAnalyzer
from trading_signals import SentimentTradingBot
from visualizer import SentimentVisualizer
import config

class CryptoSentimentBot:
    def __init__(self):
        """Initialize the crypto sentiment analysis bot"""
        print("🚀 Initializing Crypto Sentiment Analysis Bot...")
        
        self.data_collector = DataCollector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.trading_bot = SentimentTradingBot()
        self.visualizer = SentimentVisualizer()
        
        self.data_history = []
        self.analysis_history = []
        
        print("✅ Bot initialized successfully!")
    
    def collect_and_analyze(self, hours: int = 24) -> pd.DataFrame:
        """Collect data and perform sentiment analysis"""
        print(f"\n📊 Collecting data from the last {hours} hours...")
        
        # Collect data
        data = self.data_collector.get_recent_data(hours=hours)
        
        if data.empty:
            print("⚠️ No data collected. Check API configurations.")
            return pd.DataFrame()
        
        print(f"📈 Collected {len(data)} posts/tweets")
        
        # Perform sentiment analysis
        print("🧠 Performing sentiment analysis...")
        analyzed_data = self.sentiment_analyzer.analyze_dataframe(data)
        
        if not analyzed_data.empty:
            # Get sentiment statistics
            stats = self.sentiment_analyzer.get_sentiment_statistics(analyzed_data)
            print(f"📊 Sentiment Analysis Results:")
            print(f"   Mean Sentiment: {stats.get('mean_sentiment', 0):.3f}")
            print(f"   Positive Posts: {stats.get('positive_count', 0)} ({stats.get('positive_percentage', 0):.1f}%)")
            print(f"   Negative Posts: {stats.get('negative_count', 0)} ({stats.get('negative_percentage', 0):.1f}%)")
            print(f"   Neutral Posts: {stats.get('neutral_count', 0)} ({stats.get('neutral_percentage', 0):.1f}%)")
        
        return analyzed_data
    
    def generate_trading_decision(self, analyzed_data: pd.DataFrame) -> dict:
        """Generate trading decision based on sentiment analysis"""
        print("\n💰 Generating trading decision...")
        
        if analyzed_data.empty:
            return {'action': 'HOLD', 'reason': 'No data available'}
        
        # Process sentiment data and get trading decision
        decision = self.trading_bot.process_sentiment_data(analyzed_data)
        
        print(f"📈 Trading Decision: {decision['action']}")
        print(f"   Confidence: {decision.get('confidence', 0):.2f}")
        print(f"   Sentiment Score: {decision.get('sentiment_score', 0):.3f}")
        print(f"   Reason: {decision.get('reason', 'N/A')}")
        
        return decision
    
    def create_visualizations(self, analyzed_data: pd.DataFrame, save_charts: bool = True):
        """Create comprehensive visualizations"""
        print("\n📊 Creating visualizations...")
        
        if analyzed_data.empty:
            print("⚠️ No data available for visualization")
            return
        
        # Get signal history
        signal_history = self.trading_bot.signals.get_signal_history()
        
        # Create various charts
        charts_created = []
        
        # 1. Sentiment distribution
        chart_path = self.visualizer.plot_sentiment_distribution(analyzed_data, save=save_charts)
        if chart_path:
            charts_created.append(chart_path)
            print(f"   📈 Sentiment distribution chart: {os.path.basename(chart_path)}")
        
        # 2. Sentiment over time
        chart_path = self.visualizer.plot_sentiment_over_time(analyzed_data, save=save_charts)
        if chart_path:
            charts_created.append(chart_path)
            print(f"   📈 Sentiment over time chart: {os.path.basename(chart_path)}")
        
        # 3. Sentiment categories
        chart_path = self.visualizer.plot_sentiment_categories(analyzed_data, save=save_charts)
        if chart_path:
            charts_created.append(chart_path)
            print(f"   📈 Sentiment categories chart: {os.path.basename(chart_path)}")
        
        # 4. Trading signals (if any)
        if not signal_history.empty:
            chart_path = self.visualizer.plot_trading_signals(signal_history, save=save_charts)
            if chart_path:
                charts_created.append(chart_path)
                print(f"   📈 Trading signals chart: {os.path.basename(chart_path)}")
        
        # 5. Comprehensive analysis dashboard
        chart_path = self.visualizer.plot_comprehensive_analysis(analyzed_data, signal_history, save=save_charts)
        if chart_path:
            charts_created.append(chart_path)
            print(f"   📈 Comprehensive analysis dashboard: {os.path.basename(chart_path)}")
        
        print(f"✅ Created {len(charts_created)} charts")
        return charts_created
    
    def run_single_analysis(self, hours: int = 24, save_charts: bool = True):
        """Run a single analysis cycle"""
        print(f"\n{'='*60}")
        print(f"🔄 Starting Analysis Cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Step 1: Collect and analyze data
        analyzed_data = self.collect_and_analyze(hours)
        
        if analyzed_data.empty:
            print("❌ Analysis failed - no data available")
            return
        
        # Step 2: Generate trading decision
        decision = self.generate_trading_decision(analyzed_data)
        
        # Step 3: Create visualizations
        charts = self.create_visualizations(analyzed_data, save_charts)
        
        # Step 4: Store results
        self.data_history.append({
            'timestamp': datetime.now(),
            'data_count': len(analyzed_data),
            'mean_sentiment': analyzed_data['sentiment_score'].mean(),
            'decision': decision,
            'charts_created': len(charts) if charts else 0
        })
        
        print(f"\n✅ Analysis cycle completed successfully!")
        print(f"   Data points analyzed: {len(analyzed_data)}")
        print(f"   Charts created: {len(charts) if charts else 0}")
        print(f"   Trading decision: {decision['action']}")
    
    def run_continuous_monitoring(self, interval_minutes: int = 60, max_cycles: int = None):
        """Run continuous monitoring with periodic analysis"""
        print(f"\n🔄 Starting continuous monitoring (interval: {interval_minutes} minutes)")
        
        cycle_count = 0
        
        try:
            while True:
                if max_cycles and cycle_count >= max_cycles:
                    print(f"\n⏹️ Reached maximum cycles ({max_cycles}). Stopping.")
                    break
                
                cycle_count += 1
                print(f"\n🔄 Cycle {cycle_count}")
                
                # Run analysis
                self.run_single_analysis(hours=24, save_charts=True)
                
                # Wait for next cycle
                if max_cycles is None or cycle_count < max_cycles:
                    print(f"\n⏳ Waiting {interval_minutes} minutes until next cycle...")
                    time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print(f"\n⏹️ Monitoring stopped by user after {cycle_count} cycles")
        except Exception as e:
            print(f"\n❌ Error during monitoring: {e}")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print analysis summary"""
        if not self.data_history:
            print("\n📊 No analysis history available")
            return
        
        print(f"\n{'='*60}")
        print("📊 ANALYSIS SUMMARY")
        print(f"{'='*60}")
        
        # Performance metrics
        metrics = self.trading_bot.get_performance_metrics()
        if metrics:
            print(f"💰 Trading Performance:")
            print(f"   Total Trades: {metrics.get('total_trades', 0)}")
            print(f"   Buy Signals: {metrics.get('buy_trades', 0)}")
            print(f"   Sell Signals: {metrics.get('sell_trades', 0)}")
            print(f"   Average Confidence: {metrics.get('avg_confidence', 0):.3f}")
            print(f"   Average Sentiment: {metrics.get('avg_sentiment', 0):.3f}")
        
        # Analysis history
        print(f"\n📈 Analysis History:")
        print(f"   Total Analysis Cycles: {len(self.data_history)}")
        
        if self.data_history:
            total_data_points = sum(h['data_count'] for h in self.data_history)
            avg_sentiment = np.mean([h['mean_sentiment'] for h in self.data_history])
            total_charts = sum(h['charts_created'] for h in self.data_history)
            
            print(f"   Total Data Points Analyzed: {total_data_points}")
            print(f"   Average Sentiment: {avg_sentiment:.3f}")
            print(f"   Total Charts Created: {total_charts}")
            
            # Recent decisions
            recent_decisions = [h['decision']['action'] for h in self.data_history[-5:]]
            print(f"   Recent Decisions: {recent_decisions}")
    
    def demo_mode(self):
        """Run in demo mode with sample data"""
        print("\n🎭 Running in DEMO MODE with sample data...")
        
        # Create sample data
        sample_data = pd.DataFrame({
            'id': range(100),
            'text': [
                "Bitcoin is going to the moon! 🚀",
                "I'm worried about the crypto market crash",
                "Bitcoin price is stable today",
                "This is the worst investment ever",
                "Amazing gains on my crypto portfolio!",
                "Bitcoin adoption is growing rapidly",
                "I'm bullish on Bitcoin's future",
                "The market is looking bearish today",
                "Great time to buy the dip!",
                "Bitcoin will revolutionize finance"
            ] * 10,  # Repeat to get 100 entries
            'created_at': pd.date_range(start='2024-01-01', periods=100, freq='H'),
            'user': [f'user_{i}' for i in range(100)],
            'source': np.random.choice(['twitter', 'reddit'], 100),
            'retweet_count': np.random.randint(0, 100, 100),
            'favorite_count': np.random.randint(0, 50, 100),
            'score': np.random.randint(0, 1000, 100),
            'upvote_ratio': np.random.uniform(0.5, 1.0, 100)
        })
        
        # Analyze sample data
        analyzed_data = self.sentiment_analyzer.analyze_dataframe(sample_data)
        
        # Generate trading decision
        decision = self.generate_trading_decision(analyzed_data)
        
        # Create visualizations
        charts = self.create_visualizations(analyzed_data, save_charts=True)
        
        print(f"\n✅ Demo completed!")
        print(f"   Sample data points: {len(analyzed_data)}")
        print(f"   Charts created: {len(charts)}")
        print(f"   Trading decision: {decision['action']}")

def main():
    """Main function to run the crypto sentiment bot"""
    print("🚀 Crypto Sentiment Analysis Bot")
    print("=" * 50)
    
    # Initialize bot
    bot = CryptoSentimentBot()
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Crypto Sentiment Analysis Bot')
    parser.add_argument('--mode', choices=['single', 'continuous', 'demo'], 
                       default='single', help='Operation mode')
    parser.add_argument('--hours', type=int, default=24, 
                       help='Hours of data to analyze')
    parser.add_argument('--interval', type=int, default=60, 
                       help='Interval between analyses in minutes (continuous mode)')
    parser.add_argument('--max-cycles', type=int, default=None, 
                       help='Maximum number of cycles (continuous mode)')
    parser.add_argument('--no-charts', action='store_true', 
                       help='Disable chart saving')
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'demo':
            bot.demo_mode()
        elif args.mode == 'continuous':
            bot.run_continuous_monitoring(
                interval_minutes=args.interval,
                max_cycles=args.max_cycles
            )
        else:  # single mode
            bot.run_single_analysis(
                hours=args.hours,
                save_charts=not args.no_charts
            )
    
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 