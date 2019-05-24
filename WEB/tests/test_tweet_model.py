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

def test_create_timestamp():
    tweet_model.Tweet(tweet).tweet_create_timestamp(tweet)    

def test_user_location():
    tweet_model.Tweet(tweet).tweet_user_location(tweet)

def test_stated_location():
    tweet_model.Tweet(tweet).tweet_stated_location(tweet)

def test_bounding_location():
    tweet_model.Tweet(tweet).tweet_bounding_location(tweet) 

# def test_tweet_location_dictionary():
#     tweet_model.Tweet(tweet).tweet_location_dictionary(tweet_location_dictionary)            


