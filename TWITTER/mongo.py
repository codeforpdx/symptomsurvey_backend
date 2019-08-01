"""
Routines to pull tweets off a queue and write them to a mongo database
"""

import atexit
import flask_pymongo
from apscheduler.schedulers.background import BackgroundScheduler


def create_session(app, database_name, host='localhost', port=27017):
    fmt = 'mongodb://{0}:{1}/{2}'
    url = fmt.format(host, port, database_name)
    app.config['MONGO_URI'] = url
    return flask_pymongo.PyMongo(app)

class xxMongoSessionManager():
    # Store any number of sessions within the class
    sessions = dict()

    @classmethod
    def get_session(cls, database_name):
        if database_name in cls.sessions:
            return cls.sessions[database_name].session
        else:
            raise ValueError("Session {} not found".format(database_name))

    def __init__(self, app, database_name, host='localhost', port=27017):
        self.database_name = database_name
        if database_name in MongoSessionManager.sessions:
            self.session = MongoSessionManager.sessions[database_name].session
            return
        fmt = 'mongodb://{0}:{1}/{2}'
        url = fmt.format(host, port, database_name)
        app.config['MONGO_URI'] = url
        self.session = flask_pymongo.PyMongo(app)
        MongoSessionManager.sessions[database_name] = self
        return


class MongoWriter():
    def __init__(
            self,
            read_queue,
            app,
            database_name,
            host='localhost',
            port=27017):

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

    def write_tweets(self):
        count = 0
        while not self.read_queue.empty():
            tweet = self.read_queue.get(block=False)
            self.session.db.tweets.insert(tweet)
            count += 1
        print("mongo.py wrote {} tweets to mongodb".format(count))
