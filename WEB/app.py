import flask
import flask_cors
import json

from flasgger import APISpec, Schema, Swagger, fields
from controllers import router
from services import database_service
from services import auth_service


def create_app(testconfig=None):
  """Configure Flask app."""
  appInfo = {
              "swagger": "2.0",
              "info": {
                "title": "Clackamas County Health Department Symptom Surveyor",
                "description": "Data gathered from various sources related to disease symptoms",
                #"contact": {
                  #"responsibleOrganization": "ME",
                  #"responsibleDeveloper": "Me",
                  #"email": "me@me.com",
                  #"url": "www.me.com",
                #},
                "version": "0.0.1"
              },
              #"host": "mysite.com",  # overrides localhost:500
              "schemes": [
                "http",
                "https"
              ]
            }

  app = flask.Flask(__name__)
  flask_cors.CORS(app)
  Swagger(app, template=appInfo)
  # Create a mongo client that works with the flask configuration.
  if testconfig is None:
    # Load the values from the constants file.  This file contains the
    # parameters that are used for the hashing algorithim that is
    # applied to the salted passwords.
    with open('../SHARED/constants.json') as f:
      constants = json.load(f)

    # Read the private key from `./keys/token`. This file is gitignored so
    # that our private key is not checked into version control.
    with open('keys/token') as key:
      private_key = key.read()

    # Read the private key from `./keys/token`. This file is gitignored so
    # that our private key is not checked into version control.
    with open('keys/token.pub') as key:
      public_key = key.read()

    database_service.MongoSession().configure_instance(
        app,
        constants['database_name']
    )
    auth_service.AuthSession(constants['salt'], private_key, public_key)
  else:
    testconfig.start_test_session()

  router.add_routes(app)
  return app


if __name__ == '__main__':
  app = create_app()
  app.run()
