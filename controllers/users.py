import json

from services import auth, database

def add_routes(app):
  mongo = database.MongoSession().get_mongo_client()

  @app.route('/users')
  @auth.require_permission(['USER_READ'])
  def get_users():
    users = []
    for user in mongo.db.users.find():
      users.append({'profile': user['profile'], 'role': user['role']})

    return json.dumps(users), 200, {'Content-Type': 'application/json'}