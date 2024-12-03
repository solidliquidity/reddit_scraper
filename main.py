from redditscraper import RedditScraper, SentimentAnalyzer
import os
from dotenv import load_dotenv
from datetime import datetime
# Load environment variables from .env file
load_dotenv()

# Use environment variables
reddit_scraper = RedditScraper(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
    subreddit_name="wallstreetbets"
)

posts_df = reddit_scraper.fetch_posts(limit=10)
posts_df['Time Stamp'] = posts_df['Created (UTC)'].apply(lambda x: datetime.utcfromtimestamp(x))
flairs = {'Daily Discussion', 'Discussion', 'Earnings Thread', 'News'}
filtered_posts = posts_df[posts_df['Flair'].isin(flairs)].reset_index(drop=True)

detailed_post_df = reddit_scraper.fetch_detailed_post(filtered_posts.iloc[0]['Permalink'])

comments_df = reddit_scraper.fetch_comments(filtered_posts.iloc[0]['Permalink'])
comments_df['Tickers'] = comments_df['Comment Body'].apply(lambda x: list(set(re.findall(r'\b[A-Z]{2,5}\b', x))))
comments_df['Has Tickers'] = comments_df['Tickers'].apply(lambda x: len(x) > 0)
comments_with_tickers = comments_df[comments_df['Has Tickers']].reset_index(drop=True)

comments_with_tickers['Textblob Sentiment'] = comments_with_tickers['Comment Body'].apply(
    lambda x: SentimentAnalyzer.analyse_sentiment(x)
)

print(comments_with_tickers[comments_with_tickers['Textblob Sentiment'] > 0])

