import requests
import os
import copy

from services import database_service

data = {
  'grant_type': 'client_credentials'
}

def get_tweets_from_twitter():
  auth_response = requests.post('https://api.twitter.com/oauth2/token', data=data, auth=(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_ACCESS_KEY']))
  tweet_search_params = {'q': '', 'geocode': '45.209358,-122.246009,30mi', 'count': 100}
  tweet_headers = {'Authorization': 'Bearer {}'.format(auth_response.json()['access_token'])}
  print(tweet_headers)
  print(tweet_search_params)
  tweets_response = requests.get('https://api.twitter.com/1.1/search/tweets.json', params=tweet_search_params, headers=tweet_headers)
  return tweets_response.json()

def save_tweets(tweets):
  mongo = database_service.get_mongo_client()

  mongo.db.tweets.insert_many(copy.deepcopy(tweets))
