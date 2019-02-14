import flask
import flask_cors
import json

from controllers import router
from services import database_service
from services import auth_service

# configure flask app
def create_app(testconfig = None):
  app = flask.Flask(__name__)
  flask_cors.CORS(app)

  # Create a mongo client that works with the flask configuration.
  if testconfig is None:
    # Load the values from the constants file.  This file contains the parameters that are used for the
    # hashing algorithim that is applied to the salted passwords.
    with open('constants.json') as f:
      constants = json.load(f)

    # Read the private key from `./keys/token`. This file is gitignored so that our private key is not
    # checked into version control.
    with open('keys/token') as key:
      private_key = key.read()

    # Read the private key from `./keys/token`. This file is gitignored so that our private key is not
    # checked into version control.
    with open('keys/token.pub') as key:
      public_key = key.read()
      
    database_service.MongoSession().configure_instance(app, constants['database_name'])
    auth_service.AuthSession(constants['salt'], private_key, public_key)
  else:
    testconfig.start_test_session()

  router.add_routes(app)
  return app

if __name__ == '__main__':
  app = create_app()
  app.run(host="0.0.0.0")