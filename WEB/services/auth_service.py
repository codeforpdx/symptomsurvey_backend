import json
import jwt
import binascii
import hashlib
import re
import flask

from services import database_service

class AuthSession:
  instance = None

  class __AuthSession:
    def __init__(self, salt_constants, private_key, public_key):
      self.__salt_constants = salt_constants
      self.__private_key = private_key
      self.__public_key = public_key

    # Passwords will not be stored in the database.  Instead they will be encoded using a common
    # hashing algorithm and a "salt". Each user will have their own salt, which will be a uuid V4.
    # This algorithm will be applied when the user sets their password and when they log in to compare
    # the hash result to the hash of the password that's stored in the database.
    def make_hash(self, password, salt):
      dk = hashlib.pbkdf2_hmac(self.__salt_constants['algorithm'], bytes(password, 'utf-8'), bytes(salt, 'utf-8'), int(self.__salt_constants['iterations']), dklen=int(self.__salt_constants['key_length']))
      return binascii.hexlify(dk)

    def make_token(self, data):
      return jwt.encode(data, self.__private_key, algorithm='RS256').decode('utf-8')

    def validate_header(self, authorization_header, valid_permissions, mongo):
      insufficientPermissionsResponse = {'valid': False, 'error': 'Authorization header is not for user with necessary permissions.'}
      try:
        token = re.search('(?<=Bearer ).+', authorization_header).group(0)
        token_data = jwt.decode(bytes(token, 'utf-8'), self.__public_key, algorithms=['RS256'])
      except:
        return {'valid': False, 'error': 'Authorization header malformed.'}
      role = mongo.db.roles.find_one({'_id': token_data['role']})
      if role == None or role['permissions'] == None:
        return insufficientPermissionsResponse

      for permission in role['permissions']:
        if permission in valid_permissions:
          return {'valid': True}

      return insufficientPermissionsResponse

    def compare_username_password(self, user, username, password):
      return (username == user['profile']['username']) and (self.make_hash(password, user['password']['salt']) == bytes(user['password']['hash'], 'utf-8'))

  def __init__(self, salt_constants = None, private_key = None, public_key = None):
    if not AuthSession.instance:
      AuthSession.instance = AuthSession.__AuthSession(salt_constants, private_key, public_key)

  def validate_header(self, authorization_header, valid_permissions, mongo):
    return AuthSession.instance.validate_header(authorization_header, valid_permissions, mongo)
  
  def compare_username_password(self, user, username, password):
    return AuthSession.instance.compare_username_password(user, username, password)
  
  def make_token(self, data):
    return AuthSession.instance.make_token(data)

def require_permission(valid_permissions):
  mongo = database_service.get_mongo_client()
  def wrapped_method(f):
    def check_for_role(**args):
      if not 'Authorization' in flask.request.headers:
        return json.dumps({'error': 'Request is missing an authorization header.'}), 401

      authorization_header = flask.request.headers.get('Authorization')
      auth_result = AuthSession().validate_header(authorization_header, valid_permissions, mongo)
      if not auth_result['valid']:
        return json.dumps({'error': auth_result['error']}), 401
      return f(**args)
    return check_for_role
  return wrapped_method

def login_attempt(username, password):
  mongo = database_service.get_mongo_client()
  token = None
  for user in mongo.db.users.find({'profile.username': username}):
    if (AuthSession().compare_username_password(user, username, password)):
      token = AuthSession().make_token({'profile': user['profile'], 'role': user['role']})

  if token:
    return {'token': token, 'valid': True}
  
  return {'valid': False}
