import os
import requests
from dotenv import load_dotenv
from notion_client import Client as NotionClient
from datetime import datetime
import time
import json


class MyTwitterClient:
    def __init__(self):
        load_dotenv()
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        self.user_id = os.getenv("TWITTER_ACCESS_TOKEN").split('-')[0]

    def get_100_liked_tweets(self):
        url = f"https://api.twitter.com/2/users/{self.user_id}/liked_tweets"
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()['data']
        else:
            raise Exception(f"Could not fetch liked tweets: {response.status_code} {response.text}")

    def get_2000_liked_tweets(self):
        url = f"https://api.twitter.com/2/users/{self.user_id}/liked_tweets"
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        params = {"max_results": 100}  # Fetch 100 tweets at a time
        all_tweets = []

        while len(all_tweets) < 2000:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                raise Exception(f"Could not fetch liked tweets: {response.status_code} {response.text}")

            tweets = response.json()['data']
            all_tweets.extend(tweets)

            # Save the fetched tweets to a file
            with open('tweets.json', 'w') as f:
                json.dump(all_tweets, f)

            if 'next_token' in response.json()['meta']:
                params['pagination_token'] = response.json()['meta']['next_token']
            else:
                break  # No more tweets to fetch

            time.sleep(240)

        return all_tweets


class MyNotionClient:
    def __init__(self):
        load_dotenv()
        self.notion_token = os.getenv("NOTION_API_KEY")
        self.notion_database_id = os.getenv("NOTION_DATABASE_ID")
        self.client = NotionClient(auth=self.notion_token)

    def tweet_exists(self, tweet_id):
        try:
            # Query the database for a tweet with the given ID
            response = self.client.databases.query(
                database_id=self.notion_database_id,
                filter={"property": "Tweet ID", "title": {"equals": tweet_id}}
            )
            exists = len(response["results"]) > 0
            print(f"Tweet {tweet_id} exists: {exists}")
            return exists
        except Exception as e:
            print(f"Could not query the database: {e}")
            return False

    def add_tweet(self, tweet):
        try:
            # Add a new page (row) to the database
            self.client.pages.create(
                parent={"database_id": self.notion_database_id},
                properties={
                    'Tweet ID': {"title": [{"text": {"content": tweet['id']}}]},
                    'Tweet URL': {"url": f"https://twitter.com/user/status/{tweet['id']}"},
                    'Tweet text': {"rich_text": [{"text": {"content": tweet['text']}}]},
                    'Added Date': {"date": {"start": datetime.now().isoformat()}}
                }
            )
            return True
        except Exception as e:
            print(f"Could not add tweet to the database: {e}")
            return False


if __name__ == "__main__":
    twitter_client = MyTwitterClient()
    notion_client = MyNotionClient()

    try:
        liked_tweets = twitter_client.get_100_liked_tweets()

        # # Check if the tweets file exists
        # if os.path.exists('tweets.json'):
        #     # Load the tweets from the file
        #     with open('tweets.json', 'r') as f:
        #         liked_tweets = json.load(f)
        # else:
        #     # Fetch the tweets from the Twitter API
        #     liked_tweets = twitter_client.get_2000_liked_tweets()

        for tweet in liked_tweets:
            if not notion_client.tweet_exists(tweet['id']):
                notion_client.add_tweet(tweet)
                time.sleep(0.5)
    except Exception as e:
        print(e)
