import requests
from twitter_scraper import get_tweets


class XScrapper:

    def __init__(self, username):
        self.username = username

    def fetch_tweets(self, start_date, end_date):
        # Placeholder for fetching tweets within date range
        pass

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

