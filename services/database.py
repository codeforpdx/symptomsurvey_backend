import flask_pymongo

class MongoSession:
  instance = None

  class __MongoSession:
    def __init__(self):
      self.mongo = None

  def __init__(self):
    if not MongoSession.instance:
      MongoSession.instance = MongoSession.__MongoSession()

  def create_instance(self, app):
    app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/social_media_scraper'
    MongoSession.instance.mongo = flask_pymongo.PyMongo(app)

  def get_mongo_client(self):
    return MongoSession.instance.mongo
