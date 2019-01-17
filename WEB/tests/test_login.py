import json

from test_app import client

def test_bad_login(client):
  assert client.post('/login', json={'username': 'bob', 'password': 'badpw'}).data == bytes(json.dumps({'error': 'There is no user with this username and password.'}), 'utf-8')

def test_good_login(client):
  response = client.post('/login', json={'username': 'bob', 'password': 'pw'}).data.decode('utf-8')
  assert response == json.dumps({'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJwcm9maWxlIjp7InVzZXJuYW1lIjoiYm9iIiwiZmlyc3ROYW1lIjoiUm9iZXJ0IiwibGFzdE5hbWUiOiJTbWl0aCJ9LCJyb2xlIjoidXNlciJ9.OVBwW8wJGcRZHSQkwFaVqcN2dXbBAknmyYcL6tlekob4hknyB0le2idP2wK3maQPr6E4RiyKsMSVwk86Mt82YCfoK6vJVSrS237oxcWxSLCqn3OHRuJjTEbmpzqPqCrxcB2EW6dEMZ0cJlNe1NXGsdy3Wf2WcTWcOfeZ30g7Byg'})
