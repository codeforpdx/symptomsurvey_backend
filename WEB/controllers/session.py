import json
import flask

from services import auth_service

JSON_CONTENT_TYPE = {'Content-Type': 'application/json'}


def add_routes(app):
  @app.route('/login', methods=['POST'])
  def login():  # pylint: disable=unused-variable
    '''
    Login endpoint.  Checks a submitted username and password against the
    users in the users collection.
    If there is a match, the user's profile and role are put into a JSON
    Web Token (JWT) and that token is returned.
    ---
    parameters:
      - in: body
        name: body
        description: JSON name-value pair parameters consisting of username and password
        schema:
          properties:
            username:
              type: string
              description: user name.
              example: bob
            password:
              type: string
              description: password.
              example: pw
    produces:
      application/json
    responses:
      200:
        description: Successfully authenticated
        examples:
          application/json: {"token": "jwt token value elided"}
      401:
        description: Authentication failed
        examples:
          application/json: { "error" : "There is no user with this username and password."}
    '''
    body = flask.request.get_json()
    username = body['username']
    password = body['password']
    result = auth_service.login_attempt(username, password)

    if result['valid']:
      return json.dumps({'token': result['token']}), 200, JSON_CONTENT_TYPE
    msg = 'There is no user with this username and password.'
    return json.dumps({'error': msg}), 401
