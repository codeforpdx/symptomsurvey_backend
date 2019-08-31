"""
Routines to get latest tweets and write them to a queue

"""
import atexit
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
# from dateutil.parser import parse
#  import dateutil


def get_access_keys():
    """
    Read TWITTER_API environment variables and return
    them in a dictionary
    """
    twitter_keys = dict()
    msg = ""
    for env in ['TWITTER_API_ACCESS_KEY', 'TWITTER_API_KEY']:
        if env not in os.environ:
            msg += f"'{env}' not set.\n"
            continue
        twitter_keys[env] = os.environ[env]
        if len(twitter_keys[env]) < 20:
            msg += f"'{env}' not valid:{twitter_keys[env]}\n"
            continue
    if msg:
        msg = "\nFailed to read TWITTER API environment variables\n" + msg
        raise EnvironmentError(msg)
    return twitter_keys


class TwitterReader():
    _one_instance_poision = False  # Only allow one instantiation

    def __init__(self, app, write_queue, settings, latest_tweet_function):
        if TwitterReader._one_instance_poision:
            raise ValueError("Only one instance of TwitterReader allowed")
        TwitterReader._one_instance_poision = True
        self.app = app  # Flask application id
        self.write_queue = write_queue  # Tweets get written to this queue
        # Callable to retrieve currently largest Tweet
        self.settings = settings
        self.latest_tweet_function = latest_tweet_function
        self.keys = get_access_keys()

        # Set up scheduled searches to Twitter
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            func=self.get_tweets,
            trigger="interval",
            seconds=self.settings['get_interval_in_seconds'],
            max_instances=1)
        atexit.register(lambda: self.scheduler.shutdown())
        self.scheduler.start()
        return

    def get_tweets_from_twitter(self, max_id=None, since_id=None):
        auth_response = requests.post(
            'https://api.twitter.com/oauth2/token',
            data={'grant_type': 'client_credentials'},
            auth=(
                self.keys['TWITTER_API_KEY'],
                self.keys['TWITTER_API_ACCESS_KEY']
            )
        )
        as_json = auth_response.json()
        if 'errors' in as_json:
            raise EnvironmentError(as_json['errors'])
        access_token = auth_response.json()['access_token']

        tweet_search_params = {
            'q': '',
            'geocode': self.settings['geocode'],
            'count': self.settings['max_tweets_per_get']}
        if since_id is not None:
            tweet_search_params['since_id'] = since_id
        if max_id is not None:
            tweet_search_params['max_id'] = max_id
        tweet_headers = {
            'Authorization': f'Bearer {access_token}'
        }
        tweets_response = requests.get(
            'https://api.twitter.com/1.1/search/tweets.json',
            params=tweet_search_params,
            headers=tweet_headers
        )
        return tweets_response.json()

    def get_tweets(self):
        """
        Get available tweets.

        Because of the way twitter works, multiple calls might
        be needed to get all the tweets.  Therefore we loop until there
        are no longer any tweets.

        """
        print("in get tweets")
        tweets_received = 0  # Number of total Tweets during this call
        max_id_for_next_batch = None  # Used for batch search below
        since_id = self.latest_tweet_function()['id']
        print("since_id (latest tweet) is ", since_id)
        latest_id = 0
        while True:
            # Get next batch of tweets
            kwargs = {
                'since_id': since_id,
                'max_id': max_id_for_next_batch
            }
            tweets_response = self.get_tweets_from_twitter(**kwargs)
            # Validate that there are tweets to process further.
            if 'errors' in tweets_response.keys():
                print(tweets_response['errors'])
                print(kwargs)
                raise ValueError(str(tweets_response))
            tweets = tweets_response['statuses']
            num_tweets_in_response = len(tweets)
            if len(tweets) == 0:
                break
            for tweet in tweets:
                self.write_queue.put(tweet)
            # Update working variables based on tweets received.
            ids = [tweet['id'] for tweet in tweets]
            max_id_for_next_batch = min(ids) - 1
            latest_id = max(latest_id, max(ids))
            tweets_received += num_tweets_in_response
            print("Most recent tweets:")
            for tweet in tweets[:5]:
                print(tweet['id'], tweet['text'][:80])
            if tweets_received > self.settings['max_historical_tweets']:
                print("Warning:  Not all tweets were collected")
                print("We hit the max_historical_tweets limit")
                break
        print(f"twitter.py found {tweets_received} tweets")
