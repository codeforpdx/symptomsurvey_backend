import flask
import json
import flask_pymongo
import hashlib
import binascii
import jwt
from pprint import pprint

with open('constants.json') as f:
    salt_constants = json.load(f)

with open('keys/token') as key:
    private_key = key.read()

with open('keys/token.pub') as key:
    public_key = key

def make_hash(password, salt):
  dk = hashlib.pbkdf2_hmac(salt_constants['salt_algorithm'], bytes(password, 'utf-8'), bytes(salt, 'utf-8'), int(salt_constants['salt_iterations']), dklen=int(salt_constants['salt_key_length']))
  print(binascii.hexlify(dk))
  return binascii.hexlify(dk)

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
    if ((username == user['profile']['username']) and (make_hash(password, user['password']['salt']) == bytes(user['password']['hash'], 'utf-8'))):
      token = jwt.encode({'profile': user['profile'], 'role': user['role']}, private_key, algorithm='RS256')
      return json.dumps({'token': token.decode('utf-8')})

  return json.dumps({'error': 'There is no user with this username and password.'}), 400