import json

from services import auth_service, tweets_service

def add_routes(app):
  @app.route('/tweets/load', endpoint='load_tweets')
  # @auth_service.require_permission([])
  def load_tweets():
    tweets = tweets_service.get_tweets_from_twitter()
    try:
      tweets_service.save_tweets(tweets)
    except Exception as ex:
      return json.dumps(ex), 500, {'Content-Type': 'application/json'}
    return json.dumps(tweets), 200, {'Content-Type': 'application/json'}