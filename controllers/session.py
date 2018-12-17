import json
import flask

from services import auth

def add_routes(app, mongo):
  # Login endpoint.  Checks a submitted username and password against the users in the users collection.
  # If there is a match, the user's profile and role are put into a Json Web Token and that token is
  # returned.
  @app.route('/login', methods=['POST'])
  def login():
    body = flask.request.get_json()
    username = body['username']
    password = body['password']
    for user in mongo.db.users.find():
      if (auth.compare_username_password(user, username, password)):
        token = auth.make_token({'profile': user['profile'], 'role': user['role']})
        return json.dumps({'token': token}), 200, {'Content-Type': 'application/json'}

    return json.dumps({'error': 'There is no user with this username and password.'}), 400