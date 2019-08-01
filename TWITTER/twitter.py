"""
Routines to get latest tweets and write them to a queue

"""
from IPython import embed
import atexit
import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler
# from dateutil.parser import parse
#  import dateutil


class TwitterReader():
    _one_instance_poision = False  # Only allow one instantiation

    def __init__(self, write_queue, **kwargs):
        if TwitterReader._one_instance_poision:
            raise ValueError("Only one instance of TwitterReader allowed")
        TwitterReader._one_instance_poision = True
        self.access_key = kwargs.setdefault('TWITTER_API_ACCESS_KEY', None)
        self.key = kwargs.setdefault('TWITTER_API_KEY', None)
        self.geocode = kwargs.setdefault('geocode', None)
        self.get_interval_in_seconds = kwargs.setdefault(
            'get_interval_in_seconds',
            60
        )
        self.raw_data_database_name = kwargs.setdefault(
            'raw_data_database_name',
            'raw_tweets'
        )
        self.max_tweets_per_get = kwargs.setdefault(
            'max_tweets_per_get',
            15
        )
        self.max_historical_tweets = kwargs.setdefault(
            'max_historical_tweets',
            200
        )

        self.write_queue = write_queue  # Tweets get written to a queue
        self.runtime_filename = '../SHARED/twitter_runtime.json'
        self.load_runtime_state()

        # Set up scheduled searches to Twitter
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            func=self.get_tweets,
            trigger="interval",
            seconds=self.get_interval_in_seconds,
            max_instances=1)
        atexit.register(lambda: self.scheduler.shutdown())
        self.scheduler.start()
        return

    def load_runtime_state(self):
        " Load runtime variables from .json file "
        try:
            with open(self.runtime_filename) as f:
                runtime = json.load(f)
        except Exception:
            runtime = dict()
            runtime['latest_id'] = 0
        self.runtime = runtime

    def save_runtime_state(self):
        with open(self.runtime_filename, 'w') as f:
            json.dump(self.runtime, f, sort_keys=True, indent=4)

    def get_tweets_from_twitter(self, max_id=None, since_id=None):
        auth_response = requests.post(
            'https://api.twitter.com/oauth2/token',
            data={'grant_type': 'client_credentials'},
            auth=(self.key, self.access_key)
        )
        access_token = auth_response.json()['access_token']

        tweet_search_params = {
            'q': '',
            'geocode': self.geocode,
            'count': self.max_tweets_per_get}
        if since_id is not None:
            tweet_search_params['since_id'] = since_id
        if max_id is not None:
            tweet_search_params['max_id'] = max_id
        tweet_headers = {
            'Authorization': 'Bearer {}'.format(access_token)
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
        tweets_received = 0  # Number of total Tweets during this call
        max_id_for_next_batch = None  # Used for batch search below
        since_id = self.runtime['latest_id']
        latest_id = self.runtime['latest_id']
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
            if tweets_received > self.max_historical_tweets:
                print("Warning:  Not all tweets were collected")
                print("We hit the max_historical_tweets limit")
                break
        print("twitter.py found {} tweets".format(tweets_received))
        self.runtime['latest_id'] = latest_id
        self.save_runtime_state()
