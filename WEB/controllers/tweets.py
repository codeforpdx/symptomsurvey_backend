import json

from services import auth_service, tweets_service

def add_routes(app):
  @app.route('/tweets/load', endpoint='load_tweets')
  @auth_service.require_permission([])
  def load_tweets():
    tweets = json.dumps(tweets_service.get_tweets_from_twitter())
    tweets_service.save_tweets(tweets)
    return tweets, 200, {'Content-Type': 'application/json'}