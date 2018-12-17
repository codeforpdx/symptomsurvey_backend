import flask
import json

from services import auth

def add_routes(app, mongo):
  @app.route('/users')
  def get_users():
    authorization_header = flask.request.headers.get('Authorization')
    if not 'Authorization' in flask.request.headers:
      return json.dumps({'error': 'Request is missing an authorization header.'}), 401

    if not auth.validate_header(authorization_header):
      return json.dumps({'error': 'Request is missing valid authorization header.'}), 401

    users = []
    for user in mongo.db.users.find():
      users.append({'profile': user['profile'], 'role': user['role']})

    return json.dumps(users), 200, {'Content-Type': 'application/json'}