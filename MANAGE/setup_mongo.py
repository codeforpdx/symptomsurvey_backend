from uuid import uuid4
from pymongo import IndexModel, MongoClient, GEOSPHERE, TEXT, errors
import os
import json

from common import make_hash

dirname = os.path.dirname(__file__)

def setup_tweets(db):
    text_index = IndexModel([('text', TEXT)])
    geo_index = IndexModel([('geo', GEOSPHERE)])
    db.tweets.create_indexes([text_index, geo_index])
    
def setup_roles(db):
    with open(os.path.join(dirname, './seeds/roles.json')) as f:
        roles = json.load(f)
        insert_ignore_dupes(db.roles, roles)

def setup_users(db, salt):
    if os.environ.get('ADD_DEBUG_RECORDS') == 'True':
        print('Inserting test users into db')
        with open(os.path.join(dirname, './seeds/users.json')) as f:
            users = json.load(f)
            hasher = make_hash(salt['algorithm'], salt['iterations'], salt['key_length'])
            for user in users:
                user['password'] = hasher(user['password'], uuid4().hex)
            insert_ignore_dupes(db.users, users)

def insert_ignore_dupes(collection, records):
    try:
        collection.insert_many(records, ordered = False)
    except errors.BulkWriteError as bwe:
        pass

client = MongoClient(host = os.environ.get('MONGO_HOST'), port = int(os.environ.get('MONGO_PORT')))

settings = {}
constantsFile = os.path.join(dirname, '../SHARED/json/constants.json')
with open(constantsFile) as f:
    settings = json.load(f)

db = client[settings['database_name']]
setup_tweets(db)
setup_roles(db)
setup_users(db, settings['salt'])
