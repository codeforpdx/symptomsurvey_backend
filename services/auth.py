import json
import jwt
import binascii
import hashlib
import re

# Load the values from the constants file.  This file contains the parameters that are used for the
# hashing algorithim that is applied to the salted passwords.
with open('constants.json') as f:
    salt_constants = json.load(f)

# Read the private key from `./keys/token`. This file is gitignored so that our private key is not
# checked into version control.
with open('keys/token') as key:
    private_key = key.read()

# Read the private key from `./keys/token`. This file is gitignored so that our private key is not
# checked into version control.
with open('keys/token.pub') as key:
    public_key = key.read()

# Passwords will not be stored in the database.  Instead they will be encoded using a common
# hashing algorithm and a "salt". Each user will have their own salt, which will be a uuid V4.
# This algorithm will be applied when the user sets their password and when they log in to compare
# the hash result to the hash of the password that's stored in the database.
def make_hash(password, salt):
  dk = hashlib.pbkdf2_hmac(salt_constants['salt_algorithm'], bytes(password, 'utf-8'), bytes(salt, 'utf-8'), int(salt_constants['salt_iterations']), dklen=int(salt_constants['salt_key_length']))
  return binascii.hexlify(dk)

def compare_username_password(user, username, password):
    return (username == user['profile']['username']) and (make_hash(password, user['password']['salt']) == bytes(user['password']['hash'], 'utf-8'))

def make_token(data):
  return jwt.encode(data, private_key, algorithm='RS256').decode('utf-8')

def validate_header(authorization_header):
  token = re.search('(?<=Bearer ).+', authorization_header).group(0)
  token_data = jwt.decode(bytes(token, 'utf-8'), public_key, algorithms=['RS256'])
  return token_data['role'] in ['user', 'administrator']
