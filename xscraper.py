import tweepy
from datetime import datetime

# Twitter API credentials
API_KEY = 'your_api_key'
API_SECRET_KEY = 'your_api_secret_key'
ACCESS_TOKEN = 'your_access_token'
ACCESS_TOKEN_SECRET = 'your_access_token_secret'

# Authentication with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def fetch_tweets(username, start_date, end_date):
    """
    Fetch tweets for a given username within the specified date range.
    """
    all_tweets = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended').items():
        tweet_date = tweet.created_at
        if start_date <= tweet_date <= end_date:
            all_tweets.append(tweet)
        elif tweet_date < start_date:
            # Since tweets are fetched in reverse chronological order, break the loop if we've passed the start_date
            break
    return all_tweets


def save_tweets_to_md(tweets, filename):
    """
    Save tweets to a Markdown file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        for tweet in tweets:
            # Write tweet text
            file.write(f"{tweet.full_text}\n\n")
            # Write images if any
            if 'media' in tweet.entities:
                for media in tweet.entities['media']:
                    file.write(f"![image]({media['media_url_https']})\n\n")
            # Write URLs if any
            if 'urls' in tweet.entities:
                for url in tweet.entities['urls']:
                    file.write(f"[Link]({url['expanded_url']})\n\n")


if __name__ == "__main__":
    username = input("Enter the Twitter username: ")
    start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    end_date_str = input("Enter the end date (YYYY-MM-DD): ")

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    tweets = fetch_tweets(username, start_date, end_date)
    save_tweets_to_md(tweets, f"{username}_tweets_{start_date_str}_to_{end_date_str}.md")

    print(f"Saved tweets to {username}_tweets_{start_date_str}_to_{end_date_str}.md")
