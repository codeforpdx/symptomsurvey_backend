import json

from test_app import client

def test_bad_login(client):
  assert client.post('/login', json={'username': 'bob', 'password': 'badpw'}).data == bytes(json.dumps({'error': 'There is no user with this username and password.'}), 'utf-8')

def test_good_login(client):
  response = client.post('/login', json={'username': 'grand_magus', 'password': 'superC0Mp13x'}).data.decode('utf-8')
  assert response == json.dumps({'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJwcm9maWxlIjp7InVzZXJuYW1lIjoiZ3JhbmRfbWFndXMiLCJmaXJzdE5hbWUiOiJSZWdpbmFsZCIsImxhc3ROYW1lIjoiTWNGYW5jeXBhbnRzIn0sInJvbGUiOiJhZG1pbmlzdHJhdG9yIn0.ly954u9VOb5ol9BUkUCabLCFWLSVp67AFw6PnZuMYv3PDVxVOxxUVSTxvUt6WI5BV4VEFfIRtduuSIfmrFaUfesypTvuZkXqdlakb8oed9rSLreWPYlMeH8AOXMhAPS5tO0kRQEffY4ef77lGop96RUFiB9csZ_toZmHB3ydRb0'})
