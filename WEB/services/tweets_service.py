import requests
import os
import copy

from services import database_service

DATA = {
  'grant_type': 'client_credentials'
}
CLACKAMAS_GEO = {
  'latitude': '45.209358',
  'longitude': '-122.246009',
  'radius': '30mi'
}

def get_tweets_from_twitter(search_text = '', geolocation = CLACKAMAS_GEO):
  auth_response = requests.post('https://api.twitter.com/oauth2/token', data=DATA, auth=(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_ACCESS_KEY']))
  tweet_search_params = {'q': format_search_text(search_text), 'geocode': format_geolocation(geolocation), 'count': 100}
  tweet_headers = {'Authorization': 'Bearer {}'.format(auth_response.json()['access_token'])}
  print(tweet_headers)
  print(tweet_search_params)
  tweets_response = requests.get('https://api.twitter.com/1.1/search/tweets.json', params=tweet_search_params, headers=tweet_headers)
  return tweets_response.json()

def save_tweets(tweets):
  mongo = database_service.get_mongo_client()
  mongo.db.tweets.insert_many(copy.deepcopy(tweets))

def format_search_text(search_text = ''):
  return search_text.replace(' && ', ' ').replace(' || ',  ' OR ')

def format_geolocation(geolocation):
  if geolocation is not None:
    latitude,longitude,radius = [geolocation.get(k) for k in ('latitude', 'longitude', 'radius')]
    if latitude is not None and longitude is not None and radius is not None:
      parsed_radius = radius if 'mi' in radius or 'km' in radius else radius + 'mi'
      return f'${latitude},${longitude},${parsed_radius}'
    
    # If you wound up here then we don't have any valid input, just return empty string
    return ''
