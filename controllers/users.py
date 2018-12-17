import json

from services import auth

def add_routes(app, mongo):
  @app.route('/users')
  @auth.require_role(['administrator'])
  def get_users():
    users = []
    for user in mongo.db.users.find():
      users.append({'profile': user['profile'], 'role': user['role']})

    return json.dumps(users), 200, {'Content-Type': 'application/json'}