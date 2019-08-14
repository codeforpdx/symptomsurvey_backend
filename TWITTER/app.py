"""
Query Twitter to get tweets and save them to a database.

This query happens periodically.  Parameters are specified
in constants.json

TODO:  Put mongodb host and port in constants.json
"""

import flask
# import flask_cors
import json
import json2html
import queue
import twitter as twitter_lib
import mongo as mongo_lib
from IPython import embed
from collections import OrderedDict

def read_settings():
    """ Read in Twitter constants """
    try:
        with open('../SHARED/constants.json') as f:
            constants = json.load(f)
        settings = constants['twitter']
    except Exception:
        settings = dict()
    defaults = {
        'geocode': None,
        'get_interval_in_seconds': 60,
        'raw_data_database_name': 'raw_tweets',
        'max_tweets_per_get': 15,
        'max_historical_tweets': 200
    }
    for key, default_value in defaults.items():
        settings[key] = settings.setdefault(key, default_value)
    return settings


def tweet_to_table(json_of_tweet):
    filtered = OrderedDict()
    keys = ['id', 'created_at', 'text', ]
    for key in keys:
        filtered[key] = json_of_tweet[key]
    user = json_of_tweet['user']
    # embed()
    filtered['screen_name'] = user['screen_name']
    value = json2html.json2html.convert(json=filtered)
    return value


def add_routes(app):
    # Example route
    # TODO: remove this endpoint before this app goes into production
    @app.route('/')
    def hello_world():  # pylint: disable=unused-variable
        '''
        Default Route
        Added to ensure that the site is available and successfully installed
        ---
        responses:
        200:
            description: A simple web page of basic stats
        '''
        msg = '<p>Hello.  The Twitter service is at least somewhat alive!</p>'
        msg += '<p>Last Tweet</p>'
        latest_tweet = mongo.latest_tweet()
        msg += tweet_to_table(latest_tweet)
        msg += '<p>Mongodb server_info</p>'
        si = mongo.server_info()
        msg += json2html.json2html.convert(json=si)

        return msg


def create_app():

    # Read the private key from `./keys/token`. This file is
    # gitignored so that our private key is not checked into version
    # control.
    # with open('keys/token') as key:
    #  private_key = key.read()

    # Read the public key
    # with open('keys/token.pub') as key:
    #  public_key = key.read()

    app = flask.Flask(__name__)
    # flask_cors.CORS(app)

    # database_service.MongoSession().configure_instance(
    #           app, kwargs['raw_data_database_name'])
    # auth_service.AuthSession(constants['salt'],
    #        private_key, public_key)
    # get_and_save_tweets(**kwargs)

    add_routes(app)
    return app


#  logging.basicConfig(level=logging.INFO)
app = create_app()
app.logger.info("************ in app.py *************")
settings = read_settings()
# Set up communication from TwitterReader to MongoWriter
tweet_queue = queue.Queue()

mongo = mongo_lib.MongoWriter(
    app,
    tweet_queue,
    settings['raw_data_database_name']
)

twitter = twitter_lib.TwitterReader(
    app,
    tweet_queue,
    settings,
    mongo.latest_tweet
)

print("*******STARTING UP********")
#if __name__ == "__main__":
#    app.logger.info("Starting server")
#    app.run()
