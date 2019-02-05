import json

from test_app import client

def test_malformed_token(client):
  assert client.get('/users', headers={'authorization': 'Bearer aslkfh'}).data == bytes(json.dumps({'error': 'Authorization header malformed.'}), 'utf-8')

def test_non_admin(client):
  assert client.get('/users', headers={'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJwcm9maWxlIjp7InVzZXJuYW1lIjoiYm9iIiwiZmlyc3ROYW1lIjoiUm9iZXJ0IiwibGFzdE5hbWUiOiJTbWl0aCJ9LCJyb2xlIjoidXNlciJ9.J4uKGkWGQVornTb0UXNgH0qJB-mUiKIWoPwsbpZgrELKiRd_ZTVVcIXu91HHX8YSuFh9Go_Vq2XNxSbJkyur4X_H8Q3GeXoRt6auoeLJ3DezG_VZMyJpuMr7tdQ3c2bnWRS5-mJittfDicNBH0_vf78OV4zGTdtDOJQTHqypDsI'}).data == bytes(json.dumps({'error': 'Authorization header is not for user with necessary permissions.'}), 'utf-8')

user_data = json.dumps([
  {
    "profile": {
      "username": "bob",
      "firstName": "Robert",
      "lastName": "Smith"
    },
    "role": "user"
  },
  {
    "profile": {
      "username": "grand_magus",
      "firstName": "Reginald",
      "lastName": "McFancypants"
    },
    "role": "administrator"
  }
])

def test_admin_permissions(client):
  assert client.get('/users', headers={'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJwcm9maWxlIjp7InVzZXJuYW1lIjoiZ3JhbmRfbWFndXMiLCJmaXJzdE5hbWUiOiJSZWdpbmFsZCIsImxhc3ROYW1lIjoiTWNGYW5jeXBhbnRzIn0sInJvbGUiOiJhZG1pbmlzdHJhdG9yIn0.ly954u9VOb5ol9BUkUCabLCFWLSVp67AFw6PnZuMYv3PDVxVOxxUVSTxvUt6WI5BV4VEFfIRtduuSIfmrFaUfesypTvuZkXqdlakb8oed9rSLreWPYlMeH8AOXMhAPS5tO0kRQEffY4ef77lGop96RUFiB9csZ_toZmHB3ydRb0'}).data == bytes(user_data, 'utf-8')
