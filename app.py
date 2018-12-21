import flask
import flask_cors

from controllers import router
from services import database_service

# configure flask app
def create_app():
  app = flask.Flask(__name__)
  flask_cors.CORS(app)

  # Create a mongo client that works with the flask configuration.
  database_service.start_session(app)

  router.add_routes(app)
  return app

if __name__ == '__main__':
  app = create_app()
  app.run()