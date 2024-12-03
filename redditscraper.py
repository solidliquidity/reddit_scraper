import praw
import pandas as pd
import re
from textblob import TextBlob
from yahoo_fin import stock_info as si


class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent, subreddit_name):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.subreddit_name = subreddit_name

    def fetch_posts(self, limit=10):
        subreddit = self.reddit.subreddit(self.subreddit_name)
        posts_data = []

        for post in subreddit.hot(limit=limit):
            posts_data.append({
                "Title": post.title,
                "Score": post.score,
                "Upvote Ratio": post.upvote_ratio,
                "Number of Comments": post.num_comments,
                "Author": post.author.name if post.author else None,
                "Created (UTC)": post.created_utc,
                "URL": post.url,
                "Selftext": post.selftext,
                "Permalink": post.permalink,
                "Flair": post.link_flair_text,
                "Over 18": post.over_18,
                "Spoiler": post.spoiler,
                "Stickied": post.stickied,
                "Total Awards": post.total_awards_received,
            })

        return pd.DataFrame(posts_data)

    def fetch_detailed_post(self, permalink):
        submission = self.reddit.submission(url=f"https://www.reddit.com{permalink}")
        detailed_data = {
            "Title": submission.title,
            "Score": submission.score,
            "Upvote Ratio": submission.upvote_ratio,
            "Number of Comments": submission.num_comments,
            "Author": submission.author.name if submission.author else None,
            "Created (UTC)": submission.created_utc,
            "URL": submission.url,
            "Selftext": submission.selftext,
            "Permalink": submission.permalink,
            "Flair": submission.link_flair_text,
            "Over 18": submission.over_18,
            "Spoiler": submission.spoiler,
            "Stickied": submission.stickied,
            "Total Awards": submission.total_awards_received,
            "Edited": submission.edited,
            "Gilded": submission.gilded,
            "Distinguished": submission.distinguished,
            "View Count": submission.view_count,  # May return None
            "Subreddit": submission.subreddit.display_name,
        }

        return pd.DataFrame([detailed_data])

    def fetch_comments(self, permalink):
        submission = self.reddit.submission(url=f"https://www.reddit.com{permalink}")
        submission.comments.replace_more(limit=None)

        comments_data = []
        for comment in submission.comments.list():
            comments_data.append({
                "Post Title": submission.title,
                "Post ID": submission.id,
                "Comment ID": comment.id,
                "Comment Body": comment.body,
                "Author": comment.author.name if comment.author else None,
                "Score": comment.score,
                "Created (UTC)": comment.created_utc,
                "Is Submitter": comment.is_submitter,
                "Parent ID": comment.parent_id,
                "Permalink": comment.permalink,
            })

        return pd.DataFrame(comments_data)


class SentimentAnalyzer:
    @staticmethod
    def analyse_sentiment(text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # Polarity ranges from -1 (negative) to 1 (positive)
        return polarity


class StockInfoFetcher:
    @staticmethod
    def get_dow_tickers():
        return si.tickers_dow()

    @staticmethod
    def get_sp500_tickers():
        return si.tickers_sp500()

    @staticmethod
    def get_nasdaq_tickers():
        nasdaq_tickers = si.tickers_nasdaq()
        return set(nasdaq_tickers)

