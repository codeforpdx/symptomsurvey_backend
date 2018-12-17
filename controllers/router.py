from controllers import session

def add_routes(app, mongo):
  # Example route
  # TODO: remove this endpoint before this app goes into production
  @app.route('/')
  def hello_world():
      return 'Hello, World!'

  session.add_routes(app, mongo)
