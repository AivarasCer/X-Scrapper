import concurrent
import requests
from twitter_scraper import get_tweets
from dateutil.parser import parse as parse_date
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


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

    def filter_tweets_by_date(self, tweets):
        """
        Filters tweets to include only those within the specified start and end dates.

        Args:
            tweets (list of dict): The tweets to filter, each represented as a dictionary with a 'date' key.

        Returns:
            list of dict: The filtered tweets.
        """
        filtered_tweets = [
            tweet for tweet in tweets
            if self.start_date <= tweet['date'] <= self.end_date
        ]
        return filtered_tweets

    def extract_media(self, tweets):
        # Placeholder for extracting images and links
        pass

    def download_media(self, media_urls):
        # Create a ThreadPoolExecutor for parallel downloads
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.download_file, url): url for url in media_urls}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                else:
                    print('%r downloaded %r' % (url, len(data)))

    def download_file(self, url):
        # Function to download a file from a URL and return the content
        response = requests.get(url)
        # Check for successful response here
        return response.content

    def save_tweets_as_md(self, tweets):
        # Placeholder for saving tweets as markdown files
        pass
