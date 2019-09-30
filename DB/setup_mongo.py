from pymongo import MongoClient
from uuid import uuid4
from common import make_hash

client = MongoClient()

settings = {}
with open('../SHARED/json/constants.json') as f:
    settings = json.load(f)

db = client[settings.database_name]
setup_tweets(db)
setup_roles(db)
setup_users(db, settings.salt)

def setup_tweets(db):
    db.tweets.createIndex({text: 'text'})
    db.tweets.createIndex({geo: '2dsphere'})
    
def setup_roles(db):
    with open('./seeds/roles.json') as f:
        roles = json.load(f)
        db.roles.insert(roles)

def setup_users(db, salt):
    with open('./seeds/users.json') as f:
        users = json.load(f)
        hasher = make_hash(salt.algorithm, salt.iterations, salt.key_length)
        for user in users:
            user.pw = hasher(user.pw, uuid4())
        db.users.insert(users)    
