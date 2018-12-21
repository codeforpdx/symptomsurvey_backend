import flask
import flask_cors

from controllers import router
from services import database

# configure flask app
def create_app():
  app = flask.Flask(__name__)
  flask_cors.CORS(app)
  # TODO: add a password to the mongo database so that its contents are hidden behind this API

  # Create a mongo client that works with the flask configuration.
  database.start_session(app)

  router.add_routes(app)
  return app

if __name__ == '__main__':
  app = create_app()
  app.run()