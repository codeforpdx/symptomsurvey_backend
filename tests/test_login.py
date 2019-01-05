import json

from test_app import client

def test_login(client):
  assert client.post('/login', json={'username': 'bob', 'password': 'pw'}).data == bytes(json.dumps({'error': 'There is no user with this username and password.'}), 'utf-8')
