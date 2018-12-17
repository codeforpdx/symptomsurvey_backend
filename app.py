import flask
import flask_pymongo
import flask_cors

from controllers import router

# configure flask app
def create_app():
  app = flask.Flask(__name__)
  flask_cors.CORS(app)
  app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/social_media_scraper'
  # TODO: add a password to the mongo database so that its contents are hidden behind this API

  # Create a mongo client that works with the flask configuration.
  mongo = flask_pymongo.PyMongo(app)

  router.add_routes(app, mongo)
  return app

if __name__ == '__main__':
  app = create_app()
  app.run()