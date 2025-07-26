import praw
import os
from dotenv import load_dotenv

def test_reddit_connection():
    """Test Reddit API connection"""
    load_dotenv()
    
    # Get credentials from .env
    client_id = 'uvEfMMniF3pw0pfksu5F9A'
    client_secret = 'vuvmAB_ndrdhhY4DroUv8l0WlTnsbg'
    user_agent = os.getenv('REDDIT_USER_AGENT', 'CryptoSentimentBot/1.0')
    
    if not client_id or not client_secret:
        print("❌ Missing Reddit credentials in .env file")
        print("Please add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to your .env file")
        return False
    
    try:
        # Initialize Reddit instance
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        # Test connection by fetching a few posts
        subreddit = reddit.subreddit('cryptocurrency')
        posts = []
        
        print("🔍 Testing Reddit API connection...")
        print(f"📊 Fetching posts from r/cryptocurrency...")
        
        for post in subreddit.hot(limit=3):
            posts.append({
                'title': post.title,
                'score': post.score,
                'created_utc': post.created_utc
            })
        
        print(f"✅ Successfully connected to Reddit API!")
        print(f"📝 Fetched {len(posts)} posts")
        
        # Show sample posts
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post['title'][:80]}...")
            print(f"   Score: {post['score']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Reddit API: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your .env file has correct credentials")
        print("2. Verify your Reddit app is set to 'script' type")
        print("3. Make sure your Client ID and Secret are correct")
        return False

if __name__ == "__main__":
    test_reddit_connection() 