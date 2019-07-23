import json

from flask import request
from services import tweets_service

JSON_CONTENT_TYPE = {'Content-Type': 'application/json'}

def add_routes(app):
  @app.route('/tweets/load', endpoint='load_tweets')
  def load_tweets():  # pylint: disable=unused-variable
    '''
    Load tweets.
    Retrieve 100 tweets by users located within a given radius of the given
    latitude/longitude.
    The location is preferentially taking from the Geotagging API, but will
    fall back to their Twitter profile.
    The parameter value is specified by " latitude,longitude,radius ",
    where radius units must be specified as either " mi " (miles) or
    " km " (kilometers).
    ---
    responses:
      200:
        description: Successfully retrieved the tweets
        examples:
          application/json: {"statuses": [{"created_at": "Sun Mar 31 18:32:35 +0000 2019","id": 1112422454528524300...example tweet elided}]}
      500:
        description: Server error occurred
    '''
    tweets = tweets_service.get_tweets_from_twitter()
    data = filter_tweets(tweets)
    try:
      tweets_service.save_tweets(data)
      return json.dumps(data), 200, JSON_CONTENT_TYPE
    except Exception as ex:
      return json.dumps({'Exception': str(ex)}), 500, JSON_CONTENT_TYPE

  @app.route('/tweets', methods=['POST'])
  def getTweets():  # pylint: disable=unused-variable
    '''
    Retrieve tweets from the database based on provided search criteria.
    ---
    parameters:
      - in: body
        name: body
        description: JSON name-value pair parameter consisting of search text
        schema:
          properties:
            search:
              type: string
              description: search text
              example: Clackamas
    produces:
      application/json
    responses:
      200:
        description: Successfully retrieved the tweets
        examples:
          application/json: {"statuses": [{"created_at": "Sun Mar 31 18:32:35 +0000 2019","id": 1112422454528524300...example tweet elided}]}
      500:
        description: Server error occurred
    '''
    body = request.get_json()
    search_text = body.get('search')
    tweets = tweets_service.get_tweets_from_db(search_text)
    return tweets, 200, JSON_CONTENT_TYPE

# Takes a JSON object with tweets to extract data we need.
def filter_tweets(tweets):
  data = []
  for tweet in tweets.get("statuses", []):
    parsed_tweet = {
      "created_at": tweet.get("created_at"),
      "id": tweet.get("id"),
      "text": tweet.get("text"),
    #  "entities": tweet.get("entities"),
    #  "user": tweet.get("user"),
      "geo": tweet.get("geo"),
      "coordinates": tweet.get("coordinates"),
      "place": tweet.get("place")
    }
    data.append(parsed_tweet)
  
  return data
