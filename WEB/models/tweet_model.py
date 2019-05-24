
import os
import json
import time
from datetime import datetime

class Tweet:
    # Assumption that tweet is already converted to python via json.load

    def __init__(self, tweet): 
        self.tweet = tweet
        

    clackamas_lat_long = {
        'Clackamas':[45.407509, -122.568848],'Oregon City':[45.357819,-122.608437],
        'Happy Valley':[45.446960,-122.530838],'Milwaukie':[45.445530,-122.641663],'West Linn':[45.366718,-122.614441],
        'Canby':[45.262291,-122.692162],'Estacada':[45.289688,-122.335121],'Molalla':[45.147121,-122.575317],
        'Gladstone':[45.382198,-122.595901],'Boring':[45.430057,-122.373523],
        'Damascus':[45.417625,-122.458984], 'Beaver Creek':[45.504051,-122.386925], 'Mulino':[45.221511,-122.582033],
        'Oak Grove':[45.416239,-122.641562],'Government Camp':[45.304103,-121.754760],'Oatfield':[45.412658,-122.598009],
        'Jennings Lodge':[45.392020,-122.614704],'Johnson City':[45.404565,-122.578981],
        'Stafford':[45.357342,-122.722595],'Barlow':[45.252257,-122.721223],'Clackamas, OR':[45.407509, -122.568848],'Oregon City, OR':[45.357819,-122.608437],
        'Happy Valley, OR':[45.446960,-122.530838],'Milwaukie, OR':[45.445530,-122.641663],'West Linn, OR':[45.366718,-122.614441],
        'Canby, OR':[45.262291,-122.692162],'Estacada, OR':[45.289688,-122.335121],'Molalla, OR':[45.147121,-122.575317],
        'Gladstone, OR':[45.382198,-122.595901],'Boring, OR':[45.430057,-122.373523],
        'Damascus, OR':[45.417625,-122.458984], 'Beaver Creek, OR':[45.504051,-122.386925], 'Mulino, OR':[45.221511,-122.582033],
        'Oak Grove, OR':[45.416239,-122.641562],'Government Camp, OR':[45.304103,-121.754760],'Oatfield, OR':[45.412658,-122.598009],
        'Jennings Lodge, OR':[45.392020,-122.614704],'Johnson City, OR':[45.404565,-122.578981],
        'Stafford, OR':[45.357342,-122.722595],'Barlow, OR':[45.252257,-122.721223],
        }

    tweet_location_dictionary = {}    

    def tweet_create_timestamp(self, tweet):
        self.timestamp = tweet['created_at']
        self.tweet_location_dictionary['timestamp'] = self.timestamp
        #print(self.timestamp)
        #print(self.tweet_location_dictionary)

    def tweet_user_location(self, tweet):
        if tweet['user']['location'] in self.clackamas_lat_long:
            self.user_coordinates = self.clackamas_lat_long[tweet['user']['location']] 
            self.tweet_location_dictionary['user_coordinates'] = self.user_coordinates
            #print(self.tweet_location_dictionary)

    def tweet_stated_location(self, tweet):
        if tweet['coordinates'] != None:
            self.stated_coordinates = tweet['geo']['coordinates'] 
            #self.tweet_location_dictionary['stated_coordinates'] = self.stated_coordinates  
            #print(self.tweet_location_dictionary)

    def tweet_bounding_location(self, tweet):
        if tweet['place'] != None:
            self.bounding_coordinates = tweet['place']['bounding_box']['coordinates']      
            self.tweet_location_dictionary['bounding_coordinates'] = self.bounding_coordinates
            #print(self.tweet_location_dictionary)

    # def tweet_location_dictionary(self, tweet_location_dictionary):
    #     if not ('user_coordinates' and 'stated_coordinates' and 'bounding_coordinates') in self.tweet_location_dictionary:
            
    #         pass
        
    #     else:    
    #         #Convert back into JSON
    #         with open("data_file.json", "w") as write_file:
    #             json.dump(self.tweet_location_dictionary, write_file)



# my_dir = os.path.dirname(__file__)

# with open(my_dir + "/../../MANAGE/seeds/tweets.json", "r") as tweets_json:
#     tweet_grab = json.load(tweets_json)

# tweet = tweet_grab[2]
# print(tweet)  

# Tweet_instance = Tweet(tweet)
# print(Tweet_instance.tweet_create_timestamp(tweet))
# print(Tweet_instance.tweet_user_location(tweet))
# print(Tweet_instance.tweet_stated_location(tweet))
# print(Tweet_instance.tweet_bounding_location(tweet))









