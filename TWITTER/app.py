"""
Query Twitter to get tweets and save them to a database.

This query happens periodically.  Parameters are specified
in constants.json

TODO:  Put mongodb host and port in constants.json
"""

import flask
# import flask_cors
import json
import queue
import twitter as twitter_lib
import mongo as mongo_lib


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
            description: Should return funny text
        '''
        msg = '<p>Hello.  The Twitter service is at least somewhat alive!</p>'
        qqw = mongo.session.db.tweets.find().sort('id', -1).limit(20)
        msg += '<table>'
        row_fmt = '<tr><th>{}</th><th>{}</th></tr>'
        msg += row_fmt.format('ID', 'Message')
        for m in qqw:
            msg += row_fmt.format(m['id'], m['text'])
        msg += '</table>'
        # print("foo")
        #embed()
        msg += "<p>That was all!</p>"
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
