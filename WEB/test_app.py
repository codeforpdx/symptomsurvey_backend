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


salt_constants = {
  "iterations": 100000,
  "key_length": 256,
  "algorithm": "sha256"
}

private_key = """
-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQCnao6N6Tzfduky0K0kdQTMBtTcjaMG4o7qDc+EeoM4c6rW6dck
jKMpfEoSuERfMLY5dENDMcemZYnKtu9AZmK0HSiyOFbkrpRkTmrTLoFq4btkgTAv
lY+yIJLEzQIuGN6HsrPtzcqmznFo2HpGva4pIO+cFt2jc3objJTx1jToLwIDAQAB
AoGBAJkzRWhPe0jyw8ugchDelJkv1zJM2la+lBFSugd9JP9PuZIZQqtLlzOrbQ1c
WhTRuq8w2SxwLUbzu/gpFx9TkhXNOY4CyknE9Vv8Z6IniMjEX4G6zM070yHHuii5
L8S08wtljNXTlfu6qPbTs53TprkWfgdJcZpfkho44n8lFLABAkEA11CXemX1vHsY
4xRCvnn+Wr3SyHIywpljrh/1fVY977xTchAGHoXGKN3BL55SoJfbuc6IPf4D5Uh+
2o1WWNIiLwJBAMcM+IXd5IzrEc1MBKsPf7s4fBzFiND628dYBI1/LWvhIZZe+jV1
nIiHpSWUN2zKBtzCmJIPrAyPpsp14BA2GgECQQCO0BC5CZnVm1xledHPX0E7VL7T
XxOWCYGZQ+9jY+mO8r3yYPh+FELcZkG14PBzPmZqNrgdTjetQ8mIEskb/rzXAkEA
pUCefzzlxxxNbjxjT8URTVSqrZRNbvolRo1LUlG4WuzQXq/BWGqpJyw+LkGr9hSP
t+2SjwiV1OPaHBHakHrqAQJAfzW4FWcznhPESMJp8ikjucZOJfW9zOZ2WlP/mYQY
/qwE+BBGNlDkLp0RcARdpBOPSJAERL+eEX6MIosX1iJfBA==
-----END RSA PRIVATE KEY-----
"""

public_key = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnao6N6Tzfduky0K0kdQTMBtTc
jaMG4o7qDc+EeoM4c6rW6dckjKMpfEoSuERfMLY5dENDMcemZYnKtu9AZmK0HSiy
OFbkrpRkTmrTLoFq4btkgTAvlY+yIJLEzQIuGN6HsrPtzcqmznFo2HpGva4pIO+c
Ft2jc3objJTx1jToLwIDAQAB
-----END PUBLIC KEY-----
"""

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
