import os
import tempfile
import flask_pymongo
import json
import hashlib
import binascii

import pytest
from unittest.mock import create_autospec

from app import create_app
from services import auth_service, database_service


# Load the values from the constants file.  This file contains the parameters that are used for the
# hashing algorithim that is applied to the salted passwords.
with open('../SHARED/constants.json') as f:
  salt_constants = json.load(f)['salt']

with open('keys/token') as key:
  private_key = key.read()

with open('keys/token.pub') as key:
  public_key = key.read()

def get_nested_key(dictionary, key_list):
  result = dictionary
  for key in key_list.split('.'):
    if not result.get(key):
      return None
    else:
      result = result.get(key)

  return result

def search_datum(search, datum):
  for key in search.keys():
    if get_nested_key(datum, key) != search[key]:
      return False
  
  return True

class Collection:
  def __init__(self, data):
    self.data = data

  def find(self, search = None):
    if not search:
      return self.data

    result = []
    for datum in self.data:
      if search_datum(search, datum):
        result.append(datum)
    
    return result

  def find_one(self, search):
    for datum in self.data:
      if search_datum(search, datum):
        return datum

class UsersCollection(Collection):
  def __init__(self):
    with open('../MANAGE/seeds/users.json') as seed:
      base_data = json.load(seed)
    
    data = []
    for user in base_data:
      new_user = user
      salt = 'thing'
      new_user['password'] = {'salt': salt, 'hash': binascii.hexlify(hashlib.pbkdf2_hmac(salt_constants['algorithm'], bytes(user['password'], 'utf-8'), bytes(salt, 'utf-8'), int(salt_constants['iterations']), dklen=int(salt_constants['key_length']))).decode('utf-8')}
      data.append(new_user)
  
    Collection.__init__(self, data)


class RolesCollection(Collection):
  def __init__(self):
    with open('../MANAGE/seeds/roles.json') as seed:
      data = json.load(seed)
    
    Collection.__init__(self, data)


class Database:
  def __init__(self):
    self.users = UsersCollection()
    self.roles = RolesCollection()

class TestConfig:
  # TODO: add config for auth service to use for getting constants/keys during testing
  class __MongoSession:
    class __MongoClient:
      def __init__(self):
        self.db = Database()

    def __init__(self):
      self.mongo = self.__MongoClient()

  def start_test_session(self):
    database_service.MongoSession(self.__MongoSession())
    auth_service.AuthSession(salt_constants, private_key, public_key)

@pytest.fixture(scope='session')
def client():
  return create_app(testconfig = TestConfig()).test_client()

def test_root_path(client):
  result = client.get('/')
  assert result.data == b'Hello, World!'
  assert result.status == '200 OK'
