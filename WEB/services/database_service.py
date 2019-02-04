import flask_pymongo
import os
import json

class MongoSession:
  instance = None

  class __MongoSession:
    def __init__(self):
      self.mongo = None

  def __init__(self, instance=None):
    if not MongoSession.instance:
      if instance:
        MongoSession.instance = instance
      else:
        MongoSession.instance = MongoSession.__MongoSession()

  def configure_instance(self, app, database_name):
    mongo_host = os.environ.get('MONGO_HOST')
    if mongo_host is None:
      mongo_host = 'localhost'

    mongo_port = os.environ.get('MONGO_PORT')
    if mongo_port is None:
      mongo_port = 27017

    # TODO: add a password to the mongo database so that its contents are hidden behind this API
    app.config['MONGO_URI'] = 'mongodb://{0}:{1}/{2}'.format(mongo_host, mongo_port, database_name)
    MongoSession.instance.mongo = flask_pymongo.PyMongo(app)

  def get_mongo_client(self):
    return MongoSession.instance.mongo

def get_mongo_client():
  return MongoSession().get_mongo_client()
