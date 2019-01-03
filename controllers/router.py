from controllers import session, users

def add_routes(app):
  # Example route
  # TODO: remove this endpoint before this app goes into production
  @app.route('/')
  def hello_world():
      return 'Hello, World!'

  session.add_routes(app)
  users.add_routes(app)
