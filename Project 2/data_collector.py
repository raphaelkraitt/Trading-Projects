import tweepy
import praw
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import List, Dict, Optional
import config

class DataCollector:
    def __init__(self):
        self.twitter_api = None
        self.reddit_api = None
        self._initialize_apis()
    
    def _initialize_apis(self):
        """Initialize Twitter and Reddit APIs"""
        # Initialize Twitter API
        if all([config.TWITTER_API_KEY, config.TWITTER_API_SECRET, 
                config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET]):
            try:
                auth = tweepy.OAuthHandler(config.TWITTER_API_KEY, config.TWITTER_API_SECRET)
                auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
                self.twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
                print("Twitter API initialized successfully")
            except Exception as e:
                print(f"Failed to initialize Twitter API: {e}")
        
        # Initialize Reddit API
        if all([config.REDDIT_CLIENT_ID, config.REDDIT_CLIENT_SECRET]):
            try:
                self.reddit_api = praw.Reddit(
                    client_id=config.REDDIT_CLIENT_ID,
                    client_secret=config.REDDIT_CLIENT_SECRET,
                    user_agent=config.REDDIT_USER_AGENT
                )
                print("Reddit API initialized successfully")
            except Exception as e:
                print(f"Failed to initialize Reddit API: {e}")
    
    def collect_tweets(self, query: str = "bitcoin", max_tweets: int = None) -> pd.DataFrame:
        """Collect tweets about Bitcoin/crypto"""
        if not self.twitter_api:
            print("Twitter API not available")
            return pd.DataFrame()
        
        if max_tweets is None:
            max_tweets = config.MAX_TWEETS_PER_QUERY
        
        tweets_data = []
        try:
            # Search for tweets
            tweets = tweepy.Cursor(
                self.twitter_api.search_tweets,
                q=query,
                lang="en",
                tweet_mode="extended"
            ).items(max_tweets)
            
            for tweet in tweets:
                tweets_data.append({
                    'id': tweet.id,
                    'text': tweet.full_text,
                    'created_at': tweet.created_at,
                    'user': tweet.user.screen_name,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count,
                    'source': 'twitter'
                })
            
            print(f"Collected {len(tweets_data)} tweets")
            return pd.DataFrame(tweets_data)
            
        except Exception as e:
            print(f"Error collecting tweets: {e}")
            return pd.DataFrame()
    
    def collect_reddit_posts(self, subreddit_name: str = "Bitcoin", max_posts: int = None) -> pd.DataFrame:
        """Collect Reddit posts about Bitcoin/crypto"""
        if not self.reddit_api:
            print("Reddit API not available")
            return pd.DataFrame()
        
        if max_posts is None:
            max_posts = config.MAX_REDDIT_POSTS_PER_QUERY
        
        posts_data = []
        try:
            subreddit = self.reddit_api.subreddit(subreddit_name)
            
            # Get hot posts
            for post in subreddit.hot(limit=max_posts):
                posts_data.append({
                    'id': post.id,
                    'text': f"{post.title} {post.selftext}",
                    'created_at': datetime.fromtimestamp(post.created_utc),
                    'user': str(post.author) if post.author else 'deleted',
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'source': 'reddit'
                })
            
            print(f"Collected {len(posts_data)} Reddit posts")
            return pd.DataFrame(posts_data)
            
        except Exception as e:
            print(f"Error collecting Reddit posts: {e}")
            return pd.DataFrame()
    
    def collect_all_data(self) -> pd.DataFrame:
        """Collect data from all sources"""
        all_data = []
        
        # Collect tweets
        for keyword in config.QUERY_KEYWORDS:
            tweets_df = self.collect_tweets(keyword)
            if not tweets_df.empty:
                all_data.append(tweets_df)
        
        # Collect Reddit posts
        reddit_df = self.collect_reddit_posts()
        if not reddit_df.empty:
            all_data.append(reddit_df)
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=['id'])
            combined_df = combined_df.sort_values('created_at', ascending=False)
            return combined_df
        
        return pd.DataFrame()
    
    def get_recent_data(self, hours: int = 24) -> pd.DataFrame:
        """Get data from the last N hours"""
        all_data = self.collect_all_data()
        
        if all_data.empty:
            return all_data
        
        # Filter by time
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_data = all_data[all_data['created_at'] >= cutoff_time]
        
        print(f"Found {len(recent_data)} recent posts/tweets")
        return recent_data

if __name__ == "__main__":
    # Test the data collector
    collector = DataCollector()
    recent_data = collector.get_recent_data(hours=1)
    print(f"Collected {len(recent_data)} recent posts")
    if not recent_data.empty:
        print(recent_data.head()) 