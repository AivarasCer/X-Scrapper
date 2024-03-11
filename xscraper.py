import requests
from twitter_scraper import get_tweets
from dateutil.parser import parse as parse_date
from datetime import datetime


class XScrapper:

    def __init__(self, username, start_date_str, end_date_str, date_format='%Y-%m-%d'):
        self.username = username
        self.start_date = datetime.strptime(start_date_str, date_format).date()
        self.end_date = datetime.strptime(end_date_str, date_format).date()

    def fetch_tweets(self):
        tweets = []
        for tweet in get_tweets(self.username, pages=25):  # Example: Incrementally fetch tweets 25 pages at a time
            tweet_date = parse_date(tweet['time'])  # Assuming 'time' is the key and it's in a parseable format
            if self.start_date <= tweet_date.date() <= self.end_date:
                tweets.append(tweet)
            elif tweet_date.date() < self.start_date:
                break  # Stop fetching more tweets as we've passed the start date
        return tweets

    def filter_tweets_by_date(self, tweets, start_date, end_date):
        # Placeholder for filtering tweets by start and end date
        pass

    def extract_media(self, tweets):
        # Placeholder for extracting images and links
        pass

    def download_media(self, url, path):
        # Placeholder for downloading images and saving files
        pass

    def save_tweets_as_md(self, tweets):
        # Placeholder for saving tweets as markdown files
        pass
