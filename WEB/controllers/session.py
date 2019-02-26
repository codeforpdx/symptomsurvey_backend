import json
import flask

from services import auth_service, database_service

def add_routes(app):
  mongo = database_service.get_mongo_client()
  # Login endpoint.  Checks a submitted username and password against the users in the users collection.
  # If there is a match, the user's profile and role are put into a Json Web Token and that token is
  # returned.
  @app.route('/login', methods=['POST'])
  def login():
    '''
    Login endpoint.  Checks a submitted username and password against the users in the users collection.
    If there is a match, the user's profile and role are put into a Json Web Token and that token is
    returned.
    ---
    definitions:
      Login:
        type : object
        properties:          
          password:
            type: string
          username:
            type: string
      Token:
        type: object
        properties:
          token:
            type: string
      Error:
        type: object
        properties:
          error:
            type: string
    parameters:
        - name: login
          in: body
          type: object
          required: true
          schema:
            $ref: '#/definitions/Login'
    responses:
      200:
        description: Successfully authenticated
        schema:
          $ref: '#/definitions/Token'
        examples: 
          token: '*elided_token_value*'
      401:
        description: Authentication failed
        schema:
          $ref: '#/definitions/Error'
        examples:
          error: 'There is no user with this username and password.'      
    '''
    body = flask.request.get_json()
    username = body['username']
    password = body['password']
    result = auth_service.login_attempt(username, password)

    if result['valid']:
      return json.dumps({'token': result['token']}), 200, {'Content-Type': 'application/json'}

    return json.dumps({'error': 'There is no user with this username and password.'}), 401