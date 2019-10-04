import json

from services import auth_service, users_service

JSON_CONTENT_TYPE = {'Content-Type': 'application/json'}


def add_routes(app):
  @app.route('/users', endpoint='get_users')
  @auth_service.require_permission(['USER_READ'])
  def get_users():  # pylint: disable=unused-variable
    '''
    Retrieves registered users.
    ---
    responses:
      200:
        description: JSON Dump of users
    '''
    return json.dumps(users_service.get_all()), 200, JSON_CONTENT_TYPE
