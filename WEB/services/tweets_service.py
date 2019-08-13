from services import database_service
from bson.json_util import dumps

<<<<<<< HEAD

def get_tweets_from_db(search_text=None, limit=100):
    """ Retrieve Tweets from Database. """
    mongo = database_service.get_mongo_client()
    matching_tweets = mongo.db.tweets.find(
        format_db_search(search_text)
    ).sort('id', -1).limit(limit)
    return list(matching_tweets)


def format_db_search(search_text):
    if search_text is not None:
        return {'$text': {'$search': search_text}}
    else:
        return {}
=======
data = {
    'grant_type': 'client_credentials'
}


def get_tweets_from_twitter():
  auth_response = requests.post(
      'https://api.twitter.com/oauth2/token',
      data=data,
      auth=(
          os.environ['TWITTER_API_KEY'],
          os.environ['TWITTER_API_ACCESS_KEY']
      )
  )
  tweet_search_params = {
      'q': '',
      'geocode': '45.209358,-122.246009,30mi',
      'count': 100}
  access_token = auth_response.json()['access_token']
  tweet_headers = {
      'Authorization': 'Bearer {}'.format(access_token)
  }
  print(tweet_headers)
  print(tweet_search_params)
  tweets_response = requests.get(
      'https://api.twitter.com/1.1/search/tweets.json',
      params=tweet_search_params,
      headers=tweet_headers
  )
  return tweets_response.json()


def get_tweets_from_db(search_text):
  mongo = database_service.get_mongo_client()
  matching_tweets = mongo.db.tweets.find(format_db_search(search_text))
  return dumps(list(matching_tweets))


def save_tweets(tweets):
  mongo = database_service.get_mongo_client()
  mongo.db.tweets.insert_many(copy.deepcopy(tweets))


def format_db_search(search_text):
  if search_text is not None:
    return {'$text': {'$search': search_text}}
  else:
    return {}
>>>>>>> b08cf8e459538ad9ac0b9c25d37638e081da949f
