"""
Query Twitter to get tweets and save them to a database.

This query happens periodically.  Parameters are specified
in constants.json

TODO:  Put mongodb host and port in constants.json
"""

import flask
# import flask_cors
import json
import logging
import os
import queue
import twitter as twitter_lib
import mongo as mongo_lib


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
        msg = 'Hello.  The Twitter service is at least somewhat alive!'
        #with open('../SHARED/constants.json') as f:
        #    constants = json.load(f)
        #kwargs = constants['twitter']
        qqw = db_sess.db.tweets.find({})
        msg += str(qqw)
        #msg += str(db_sess)
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

# Read in run parameters from several sources
with open('../SHARED/constants.json') as f:
    constants = json.load(f)
kwargs = constants['twitter']
kwargs['TWITTER_API_ACCESS_KEY'] = os.environ.setdefault(
    'TWITTER_API_ACCESS_KEY',
    None
)
kwargs['TWITTER_API_KEY'] = os.environ.setdefault(
    'TWITTER_API_KEY',
    None
)

app.logger.info("************ in app.py *************")

db_sess = mongo_lib.create_session(
    app,
    kwargs['raw_data_database_name'],
    host='localhost',
    port=27017
)

tweet_queue = queue.Queue()

twitter = twitter_lib.TwitterReader(
    tweet_queue,
    **kwargs)
mongo = mongo_lib.MongoWriter(
    tweet_queue,
    app,
    kwargs['raw_data_database_name'],
    host='localhost',
    port=27017)

app.logger.info("Starting server")
app.run()
