import json
import flask

from services import auth_service, database_service

def add_routes(app):
  mongo = database_service.get_mongo_client()
  # Login endpoint.  Checks a submitted username and password against the users in the users collection.
  # If there is a match, the user's profile and role are put into a Json Web Token and that token is
  # returned.
  @app.route('/login', methods=['POST'])
  def login():
    body = flask.request.get_json()
    username = body['username']
    password = body['password']
    result = auth_service.login_attempt(username, password)

    if result['valid']:
      return json.dumps({'token': result['token']}), 200, {'Content-Type': 'application/json'}

    return json.dumps({'error': 'There is no user with this username and password.'}), 400