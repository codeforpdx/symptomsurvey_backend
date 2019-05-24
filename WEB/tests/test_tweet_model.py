import json
import os
from models import tweet_model

my_dir = os.path.dirname(__file__)

with open(my_dir + "/../../MANAGE/seeds/tweets.json", "r") as tweets_json:
    tweet_grab = json.load(tweets_json)

# assert tests if statements are true, write

tweet = tweet_grab[0]    
def test_create_tweet_instance():
    tweet_model.Tweet(tweet)

def test_user_location():
    assert tweet_model.Tweet(tweet).tweet_user_location(tweet)


