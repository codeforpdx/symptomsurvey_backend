import flask
import json
import flask_pymongo
import hashlib
import binascii
import jwt
import flask_cors

# Load the values from the constants file.  This file contains the parameters that are used for the
# hashing algorithim that is applied to the salted passwords.
with open('constants.json') as f:
    salt_constants = json.load(f)

# Read the private key from `./keys/token`. This file is gitignored so that our private key is not
# checked into version control.
with open('keys/token') as key:
    private_key = key.read()

# Passwords will not be stored in the database.  Instead they will be encoded using a common
# hashing algorithm and a "salt". Each user will have their own salt, which will be a uuid V4.
# This algorithm will be applied when the user sets their password and when they log in to compare
# the hash result to the hash of the password that's stored in the database.
def make_hash(password, salt):
  dk = hashlib.pbkdf2_hmac(salt_constants['salt_algorithm'], bytes(password, 'utf-8'), bytes(salt, 'utf-8'), int(salt_constants['salt_iterations']), dklen=int(salt_constants['salt_key_length']))
  return binascii.hexlify(dk)

# configure flask app
app = flask.Flask(__name__)
flask_cors.CORS(app)
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/social_media_scraper'
# TODO: add a password to the mongo database so that its contents are hidden behind this API

# Create a mongo client that works with the flask configuration.
mongo = flask_pymongo.PyMongo(app)

# Example route
# TODO: remove this endpoint before this app goes into production
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Login endpoint.  Checks a submitted username and password against the users in the users collection.
# If there is a match, the user's profile and role are put into a Json Web Token and that token is
# returned.
@app.route('/login', methods=['POST'])
def login():
  body = flask.request.get_json()
  username = body['username']
  password = body['password']
  for user in mongo.db.users.find():
    if ((username == user['profile']['username']) and (make_hash(password, user['password']['salt']) == bytes(user['password']['hash'], 'utf-8'))):
      token = jwt.encode({'profile': user['profile'], 'role': user['role']}, private_key, algorithm='RS256')
      return json.dumps({'token': token.decode('utf-8')}), 200, {'Content-Type': 'application/json'}

  return json.dumps({'error': 'There is no user with this username and password.'}), 400
