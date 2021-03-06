"""
Routines to pull tweets off a queue and write them to a mongo database
"""

import atexit
import flask_pymongo
import os
import textwrap
from apscheduler.schedulers.background import BackgroundScheduler
from IPython import embed


def get_host_and_port():
    """
    Returns host and port of mongodb that we should connect to.
    Within the container, docker-compose has send the environment
    variables.  On the host, we should not.  This is because to
    the host, the mongod is at 'localhost' and inside other
    containers, it is at 'mongo'
    """
    mongo_host = os.environ.setdefault('MONGO_HOST', 'localhost')
    mongo_port = os.environ.get('MONGO_PORT', 27017)
    return mongo_host, mongo_port


def create_session(app, database_name, host=None, port=None):
    if host is None or port is None:
        host, port = get_host_and_port()
        print(f"mongodb host and port set to {host}:{port}")
    url = f"mongodb://{host}:{port}/{database_name}"
    app.config['MONGO_URI'] = url
    sess = flask_pymongo.PyMongo(app, serverSelectionTimeoutMS=5000)
    SSTE = flask_pymongo.pymongo.errors.ServerSelectionTimeoutError
    try:
        print("Confirming connection to mongodb...", end='', flush=True)
    except SSTE as e:
        msg = textwrap.dedent(f"""\
            {str(e)}

            Cannot connect to mongodb.
            Tried using MONGO_URI of {url}
            """)
        raise SSTE(msg) from None
    print("Connected!", flush=True)
    return sess


class MongoWriter():
    """
    Periodically check the input queue for new Tweets, then write
    any found to the mongo db.
    """
    def __init__(
            self,
            app,
            read_queue,
            database_name,
            host=None,
            port=None):
        self.app = app
        self.database_name = database_name
        self.session = create_session(
            app,
            database_name,
            host,
            port
        )
        self.read_queue = read_queue
        # Set up scheduled write to mongodb
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            func=self.write_tweets,
            trigger="interval",
            seconds=12,
            max_instances=1)
        atexit.register(lambda: self.scheduler.shutdown())
        self.scheduler.start()
        return

    def latest_tweet(self):
        lid = self.session.db.tweets.find().sort('id', -1).limit(1)[0]
        return lid

    def server_info(self):
        return self.session.cx.server_info()

    def write_tweets(self):
        count = 0
        while not self.read_queue.empty():
            tweet = self.read_queue.get(block=False)
            # print("In write_tweets")
            # embed()
            self.session.db.tweets.insert(tweet)
            count += 1
        print(f"mongo.py wrote {count} tweets to mongodb")


if __name__ == '__main__':
    print("What host/port does mongo.py think mongodb is on...")
    host, port = get_host_and_port()
    print(f"{host}:{port}")
