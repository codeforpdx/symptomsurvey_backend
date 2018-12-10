import flask
import json
app = flask.Flask(__name__)
request = flask.request

@app.route('/')
def hello_world():
    return 'Hello, World!'

user_profile = {
  'username': 'bob',
  'password': 'pw',
  'firstName': 'Robert',
  'lastName': 'Smith'
}

@app.route('/login', methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']
  if ((username != user_profile['username']) or (password != user_profile['password'])):
    return json.dumps({'error': 'There is no user with this username and password.'}), 400
  
  return json.dumps(user_profile)