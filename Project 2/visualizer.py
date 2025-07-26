import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from typing import Dict, List
import config

class SentimentVisualizer:
    def __init__(self):
        self.setup_style()
        self.chart_path = config.CHART_SAVE_PATH
        self.ensure_chart_directory()
    
    def setup_style(self):
        """Setup matplotlib style for better looking charts"""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
    
    def ensure_chart_directory(self):
        """Ensure the chart directory exists"""
        if not os.path.exists(self.chart_path):
            os.makedirs(self.chart_path)
    
    def plot_sentiment_distribution(self, df: pd.DataFrame, save: bool = True) -> str:
        """Plot sentiment score distribution"""
        if df.empty or 'sentiment_score' not in df.columns:
            return ""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Histogram
        ax1.hist(df['sentiment_score'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.axvline(df['sentiment_score'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df["sentiment_score"].mean():.3f}')
        ax1.axvline(df['sentiment_score'].median(), color='green', linestyle='--', 
                   label=f'Median: {df["sentiment_score"].median():.3f}')
        ax1.set_xlabel('Sentiment Score')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Sentiment Score Distribution')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Box plot by source
        if 'source' in df.columns:
            df.boxplot(column='sentiment_score', by='source', ax=ax2)
            ax2.set_title('Sentiment Score by Source')
            ax2.set_xlabel('Source')
            ax2.set_ylabel('Sentiment Score')
        else:
            ax2.boxplot(df['sentiment_score'])
            ax2.set_title('Sentiment Score Box Plot')
            ax2.set_ylabel('Sentiment Score')
        
        plt.tight_layout()
        
        if save:
            filename = f"sentiment_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{config.CHART_FORMAT}"
            filepath = os.path.join(self.chart_path, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return filepath
        else:
            plt.show()
            return ""
    
    def plot_sentiment_over_time(self, df: pd.DataFrame, time_window: str = '1H', save: bool = True) -> str:
        """Plot sentiment over time"""
        if df.empty or 'sentiment_score' not in df.columns or 'created_at' not in df.columns:
            return ""
        
        # Convert to datetime and set as index
        df_copy = df.copy()
        df_copy['created_at'] = pd.to_datetime(df_copy['created_at'])
        df_copy.set_index('created_at', inplace=True)
        
        # Resample and aggregate
        sentiment_over_time = df_copy['sentiment_score'].resample(time_window).agg([
            'mean', 'std', 'count'
        ]).fillna(0)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # Sentiment mean over time
        ax1.plot(sentiment_over_time.index, sentiment_over_time['mean'], 
                marker='o', linewidth=2, markersize=4)
        ax1.fill_between(sentiment_over_time.index, 
                        sentiment_over_time['mean'] - sentiment_over_time['std'],
                        sentiment_over_time['mean'] + sentiment_over_time['std'],
                        alpha=0.3)
        ax1.axhline(y=config.SENTIMENT_THRESHOLD_BUY, color='green', linestyle='--', 
                   label=f'Buy Threshold ({config.SENTIMENT_THRESHOLD_BUY})')
        ax1.axhline(y=config.SENTIMENT_THRESHOLD_SELL, color='red', linestyle='--', 
                   label=f'Sell Threshold ({config.SENTIMENT_THRESHOLD_SELL})')
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax1.set_ylabel('Sentiment Score')
        ax1.set_title('Sentiment Score Over Time')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Post count over time
        ax2.bar(sentiment_over_time.index, sentiment_over_time['count'], 
               alpha=0.7, color='orange')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Number of Posts')
        ax2.set_title('Post Volume Over Time')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filename = f"sentiment_over_time_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{config.CHART_FORMAT}"
            filepath = os.path.join(self.chart_path, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return filepath
        else:
            plt.show()
            return ""
    
    def plot_sentiment_categories(self, df: pd.DataFrame, save: bool = True) -> str:
        """Plot sentiment categories pie chart"""
        if df.empty or 'sentiment_category' not in df.columns:
            return ""
        
        category_counts = df['sentiment_category'].value_counts()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Pie chart
        colors = ['lightgreen', 'lightcoral', 'lightblue']
        wedges, texts, autotexts = ax1.pie(category_counts.values, labels=category_counts.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Sentiment Category Distribution')
        
        # Bar chart
        category_counts.plot(kind='bar', ax=ax2, color=colors)
        ax2.set_title('Sentiment Category Counts')
        ax2.set_xlabel('Sentiment Category')
        ax2.set_ylabel('Count')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save:
            filename = f"sentiment_categories_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{config.CHART_FORMAT}"
            filepath = os.path.join(self.chart_path, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return filepath
        else:
            plt.show()
            return ""
    
    def plot_trading_signals(self, signal_df: pd.DataFrame, save: bool = True) -> str:
        """Plot trading signals over time"""
        if signal_df.empty:
            return ""
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # Convert timestamp to datetime if needed
        signal_df_copy = signal_df.copy()
        signal_df_copy['timestamp'] = pd.to_datetime(signal_df_copy['timestamp'])
        signal_df_copy.set_index('timestamp', inplace=True)
        
        # Sentiment scores with signals
        ax1.plot(signal_df_copy.index, signal_df_copy['sentiment_score'], 
                marker='o', linewidth=2, markersize=6, label='Sentiment Score')
        
        # Mark buy signals
        buy_signals = signal_df_copy[signal_df_copy['signal'] == 'BUY']
        if not buy_signals.empty:
            ax1.scatter(buy_signals.index, buy_signals['sentiment_score'], 
                       color='green', s=100, marker='^', label='BUY Signal', zorder=5)
        
        # Mark sell signals
        sell_signals = signal_df_copy[signal_df_copy['signal'] == 'SELL']
        if not sell_signals.empty:
            ax1.scatter(sell_signals.index, sell_signals['sentiment_score'], 
                       color='red', s=100, marker='v', label='SELL Signal', zorder=5)
        
        # Threshold lines
        ax1.axhline(y=config.SENTIMENT_THRESHOLD_BUY, color='green', linestyle='--', 
                   label=f'Buy Threshold ({config.SENTIMENT_THRESHOLD_BUY})')
        ax1.axhline(y=config.SENTIMENT_THRESHOLD_SELL, color='red', linestyle='--', 
                   label=f'Sell Threshold ({config.SENTIMENT_THRESHOLD_SELL})')
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        ax1.set_ylabel('Sentiment Score')
        ax1.set_title('Trading Signals Based on Sentiment')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Signal frequency
        signal_counts = signal_df_copy['signal'].value_counts()
        if not signal_counts.empty:
            signal_counts.plot(kind='bar', ax=ax2, color=['green', 'red'])
            ax2.set_title('Signal Distribution')
            ax2.set_xlabel('Signal Type')
            ax2.set_ylabel('Count')
            ax2.tick_params(axis='x', rotation=0)
        
        plt.tight_layout()
        
        if save:
            filename = f"trading_signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{config.CHART_FORMAT}"
            filepath = os.path.join(self.chart_path, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return filepath
        else:
            plt.show()
            return ""
    
    def plot_comprehensive_analysis(self, df: pd.DataFrame, signal_df: pd.DataFrame = None, save: bool = True) -> str:
        """Create a comprehensive analysis dashboard"""
        if df.empty:
            return ""
        
        fig = plt.figure(figsize=(20, 16))
        
        # Create subplots
        gs = fig.add_gridspec(4, 3, hspace=0.3, wspace=0.3)
        
        # 1. Sentiment distribution
        ax1 = fig.add_subplot(gs[0, 0])
        df['sentiment_score'].hist(bins=30, alpha=0.7, color='skyblue', edgecolor='black', ax=ax1)
        ax1.axvline(df['sentiment_score'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df["sentiment_score"].mean():.3f}')
        ax1.set_title('Sentiment Distribution')
        ax1.legend()
        
        # 2. Sentiment by source
        ax2 = fig.add_subplot(gs[0, 1])
        if 'source' in df.columns:
            df.boxplot(column='sentiment_score', by='source', ax=ax2)
            ax2.set_title('Sentiment by Source')
        else:
            ax2.text(0.5, 0.5, 'No source data', ha='center', va='center', transform=ax2.transAxes)
            ax2.set_title('Sentiment by Source')
        
        # 3. Sentiment categories
        ax3 = fig.add_subplot(gs[0, 2])
        if 'sentiment_category' in df.columns:
            category_counts = df['sentiment_category'].value_counts()
            colors = ['lightgreen', 'lightcoral', 'lightblue']
            ax3.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', colors=colors)
            ax3.set_title('Sentiment Categories')
        
        # 4. Sentiment over time (full width)
        ax4 = fig.add_subplot(gs[1, :])
        if 'created_at' in df.columns:
            df_copy = df.copy()
            df_copy['created_at'] = pd.to_datetime(df_copy['created_at'])
            df_copy.set_index('created_at', inplace=True)
            
            sentiment_over_time = df_copy['sentiment_score'].resample('1H').mean().fillna(0)
            ax4.plot(sentiment_over_time.index, sentiment_over_time.values, marker='o', linewidth=2)
            ax4.axhline(y=config.SENTIMENT_THRESHOLD_BUY, color='green', linestyle='--', 
                       label=f'Buy Threshold ({config.SENTIMENT_THRESHOLD_BUY})')
            ax4.axhline(y=config.SENTIMENT_THRESHOLD_SELL, color='red', linestyle='--', 
                       label=f'Sell Threshold ({config.SENTIMENT_THRESHOLD_SELL})')
            ax4.set_title('Sentiment Over Time')
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        
        # 5. Trading signals (if available)
        if signal_df is not None and not signal_df.empty:
            ax5 = fig.add_subplot(gs[2, :])
            signal_df_copy = signal_df.copy()
            signal_df_copy['timestamp'] = pd.to_datetime(signal_df_copy['timestamp'])
            signal_df_copy.set_index('timestamp', inplace=True)
            
            ax5.plot(signal_df_copy.index, signal_df_copy['sentiment_score'], 
                    marker='o', linewidth=2, markersize=6, label='Sentiment Score')
            
            # Mark signals
            buy_signals = signal_df_copy[signal_df_copy['signal'] == 'BUY']
            sell_signals = signal_df_copy[signal_df_copy['signal'] == 'SELL']
            
            if not buy_signals.empty:
                ax5.scatter(buy_signals.index, buy_signals['sentiment_score'], 
                           color='green', s=100, marker='^', label='BUY Signal', zorder=5)
            if not sell_signals.empty:
                ax5.scatter(sell_signals.index, sell_signals['sentiment_score'], 
                           color='red', s=100, marker='v', label='SELL Signal', zorder=5)
            
            ax5.set_title('Trading Signals')
            ax5.legend()
            ax5.grid(True, alpha=0.3)
        
        # 6. Statistics summary
        ax6 = fig.add_subplot(gs[3, :])
        ax6.axis('off')
        
        # Calculate statistics
        stats = {
            'Total Posts': len(df),
            'Mean Sentiment': f"{df['sentiment_score'].mean():.3f}",
            'Median Sentiment': f"{df['sentiment_score'].median():.3f}",
            'Std Sentiment': f"{df['sentiment_score'].std():.3f}",
            'Positive Posts': len(df[df['sentiment_score'] > 0.1]),
            'Negative Posts': len(df[df['sentiment_score'] < -0.1]),
            'Neutral Posts': len(df[(df['sentiment_score'] >= -0.1) & (df['sentiment_score'] <= 0.1)])
        }
        
        if signal_df is not None and not signal_df.empty:
            stats.update({
                'Total Signals': len(signal_df),
                'Buy Signals': len(signal_df[signal_df['signal'] == 'BUY']),
                'Sell Signals': len(signal_df[signal_df['signal'] == 'SELL'])
            })
        
        # Create text summary
        summary_text = '\n'.join([f"{k}: {v}" for k, v in stats.items()])
        ax6.text(0.1, 0.9, 'Analysis Summary', fontsize=16, fontweight='bold', transform=ax6.transAxes)
        ax6.text(0.1, 0.8, summary_text, fontsize=12, transform=ax6.transAxes, 
                verticalalignment='top', fontfamily='monospace')
        
        if save:
            filename = f"comprehensive_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{config.CHART_FORMAT}"
            filepath = os.path.join(self.chart_path, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return filepath
        else:
            plt.show()
            return ""

if __name__ == "__main__":
    # Test the visualizer
    visualizer = SentimentVisualizer()
    
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'sentiment_score': np.random.normal(0, 0.5, 100),
        'sentiment_category': np.random.choice(['positive', 'negative', 'neutral'], 100),
        'source': np.random.choice(['twitter', 'reddit'], 100),
        'created_at': pd.date_range(start='2024-01-01', periods=100, freq='H')
    })
    
    print("Testing visualizer...")
    visualizer.plot_sentiment_distribution(sample_data, save=False)
    visualizer.plot_sentiment_categories(sample_data, save=False) 