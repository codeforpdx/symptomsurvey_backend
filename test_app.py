import os
import tempfile
import flask_pymongo

import pytest
from unittest.mock import create_autospec

from app import create_app
from services import database_service

class TestConfig:
  class __MongoSession:
    def __init__(self, app):
      self.mongo = create_autospec(flask_pymongo.PyMongo)(app)

  def start_test_session(self, app):
    database_service.MongoSession(TestConfig.__MongoSession(app))

@pytest.fixture
def client():
  return create_app(testconfig = TestConfig()).test_client()

def test_root(client):
  assert client.get('/').data == b'Hello, World!'
