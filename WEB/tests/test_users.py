import json

from test_app import client

def test_malformed_token(client):
  assert client.get('/users', headers={'authorization': 'Bearer aslkfh'}).data == bytes(json.dumps({'error': 'Authorization header malformed.'}), 'utf-8')

def test_non_admin(client):
  assert client.get('/users', headers={'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJwcm9maWxlIjp7InVzZXJuYW1lIjoiYm9iIiwiZmlyc3ROYW1lIjoiUm9iZXJ0IiwibGFzdE5hbWUiOiJTbWl0aCJ9LCJyb2xlIjoidXNlciJ9.OVBwW8wJGcRZHSQkwFaVqcN2dXbBAknmyYcL6tlekob4hknyB0le2idP2wK3maQPr6E4RiyKsMSVwk86Mt82YCfoK6vJVSrS237oxcWxSLCqn3OHRuJjTEbmpzqPqCrxcB2EW6dEMZ0cJlNe1NXGsdy3Wf2WcTWcOfeZ30g7Byg'}).data == bytes(json.dumps({'error': 'Authorization header is not for user with necessary permissions.'}), 'utf-8')

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
  assert client.get('/users', headers={'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJwcm9maWxlIjp7InVzZXJuYW1lIjoiZ3JhbmRfbWFndXMiLCJmaXJzdE5hbWUiOiJSZWdpbmFsZCIsImxhc3ROYW1lIjoiTWNGYW5jeXBhbnRzIn0sInJvbGUiOiJhZG1pbmlzdHJhdG9yIn0.SXe5GlQ3AMmGQfugfEHCFy0wdoZfLGAU34GDDcF9dIG1eIJRyx4wyTwtGpupsqPqlW3t6T1O2n55pCLlnaT5TtVohLkbpGUU5ItW_1ik3vKw401hHt_D0rNsLQUzRv4u4vv7qEOEmXQs71mxxKfm9HwjFvPQdokqmeb1XhNo3Fg'}).data == bytes(user_data, 'utf-8')
