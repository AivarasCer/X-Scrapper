import concurrent
import requests
import shelve
import re
from twitter_scraper import get_tweets
from dateutil.parser import parse as parse_date
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class XScrapper:

    def __init__(self, username, start_date_str, end_date_str, date_format='%Y-%m-%d', cache_file='tweets_cache.db'):
        self.username = username
        self.start_date = datetime.strptime(start_date_str, date_format).date()
        self.end_date = datetime.strptime(end_date_str, date_format).date()
        self.cache_file = cache_file

    def fetch_tweets(self):
        cache_key = f"{self.username}_{self.start_date}_{self.end_date}"
        tweets = []

        # Use shelve to open the cache file
        with shelve.open(self.cache_file) as cache:
            if cache_key in cache:
                print("Fetching tweets from cache.")
                return cache[cache_key]  # Return cached tweets if available

            print("Fetching tweets from Twitter.")
            for tweet in get_tweets(self.username, pages=25):
                tweet_date = parse_date(tweet['time'])
                if self.start_date <= tweet_date.date() <= self.end_date:
                    tweets.append(tweet)
                elif tweet_date.date() < self.start_date:
                    break  # Stop fetching as we've passed the start date

            cache[cache_key] = tweets  # Cache the fetched tweets
        return tweets

    def extract_media(self, tweets):
        """
        Extracts media URLs from a list of tweets.

        Args:
            tweets (list of dict): Tweets to extract media from.

        Returns:
            dict: A dictionary with tweet IDs as keys and a list of media URLs as values.
        """
        media_urls = {}
        url_pattern = r'https?://[^\s]+'

        for tweet in tweets:
            tweet_id = tweet['id']
            text = tweet['text']
            urls = re.findall(url_pattern, text)

            # Filter or process URLs as needed, e.g., expand short URLs or filter out non-media links

            media_urls[tweet_id] = urls

        return media_urls

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
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download {url}: Status code {response.status_code}")

    def save_tweets_as_md(self, tweets):
        for tweet in tweets:
            filename = f"{tweet['id']}.md"
            with open(filename, 'w') as f:
                f.write(f"# {tweet['username']}'s Tweet\n\n")
                f.write(f"{tweet['text']}\n\n")
                if 'images' in tweet:
                    for image in tweet['images']:
                        f.write(f"![Image]({image})\n")
                if 'links' in tweet:
                    for link in tweet['links']:
                        f.write(f"[Link]({link})\n")
