from controllers import session, users, tweets
import utilities

def add_routes(app):
  # Example route
  # TODO: remove this endpoint before this app goes into production
  @app.route('/')
  def hello_world():  # pylint: disable=unused-variable
    '''
    Default Route
    Added to ensure that the site is available and successfully installed
    ---
    responses:
      200:
        description: Should return 'Hello, World!'
        examples:
          string: "Hello, World!"
    '''
    return 'Hello, World!'

  @app.route('/python')
  def howdy():  # pylint: disable=unused-variable
    utilities.debug()
    return "Interactive shell"

  session.add_routes(app)
  users.add_routes(app)
  tweets.add_routes(app)
