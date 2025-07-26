import requests
import pandas as pd
from datetime import datetime, timedelta
import config

class NewsFetcher:
    def __init__(self):
        self.api_key = config.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"
    
    def fetch_news(self, query=None, max_articles=None):
        query = query or config.NEWS_QUERY
        max_articles = max_articles or config.MAX_ARTICLES
        
        # Calculate date range (last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        params = {
            'q': query,
            'from': start_date.strftime('%Y-%m-%d'),
            'to': end_date.strftime('%Y-%m-%d'),
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': max_articles,
            'apiKey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'ok':
                articles = []
                for article in data['articles']:
                    articles.append({
                        'title': article['title'],
                        'description': article['description'],
                        'published_at': article['publishedAt'],
                        'source': article['source']['name'],
                        'url': article['url']
                    })
                return pd.DataFrame(articles)
            else:
                print(f"News API error: {data.get('message', 'Unknown error')}")
                return pd.DataFrame()
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Unexpected error: {e}")
            return pd.DataFrame()

if __name__ == "__main__":
    fetcher = NewsFetcher()
    news_df = fetcher.fetch_news()
    print(f"Fetched {len(news_df)} articles")
    if not news_df.empty:
        print(news_df[['title', 'published_at']].head()) 