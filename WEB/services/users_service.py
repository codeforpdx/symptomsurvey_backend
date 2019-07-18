from services import database_service


def get_all():
  mongo = database_service.get_mongo_client()
  users = []
  for user in mongo.db.users.find():
    users.append({'profile': user['profile'], 'role': user['role']})
  return users
