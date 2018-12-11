import flask
import json
import flask_pymongo

# configure flask app
app = flask.Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/social_media_scraper'
mongo = flask_pymongo.PyMongo(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['POST'])
def login():
  username = flask.request.form['username']
  password = flask.request.form['password']
  for user in mongo.db.users.find():
    # TODO: use a salt for passwords so they aren't persisted naked.
    if ((username == user['profile']['username']) and (password == user['password'])):
      return json.dumps({'profile': user['profile'], 'role': user['role']})

  return json.dumps({'error': 'There is no user with this username and password.'}), 400