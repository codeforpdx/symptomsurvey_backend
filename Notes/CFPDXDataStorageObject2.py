import json
import time
from datetime import datetime

# clackamas_lat_long = {
#     'Clackamas':[45.407509, -122.568848],'Oregon City':[45.357819,-122.608437],
#     'Happy Valley':[45.446960,-122.530838],'Milwaukie':[45.445530,-122.641663],'West Linn'[45.366718,-122.614441],
#     'Canby':[45.262291,-122.692162],'Estacada':[45.289688,-122.335121],'Molalla':[45.147121,-122.575317],
#     'Canby':[45.262291,-122.692162], 'Gladstone':[45.382198,-122.595901],'Boring':[45.430057,-122.373523],
#     'Damascus':[45.417625,-122.458984], 'Beaver Creek':[45.504051,-122.386925], 'Mulino':[45.221511,-122.582033],
#     'Oak Grove':[45.416239,-122.641562],'Government Camp':[45.304103,-121.754760],'Oatfield':[45.412658,-122.598009],
#     'Jennings Lodge':[45.392020,-122.614704],'Johnson City':[45.404565,-122.578981],
#     'Stafford':[45.357342,-122.722595],'Barlow':[45.252257,-122.721223],
#

coordinates = []
with open("MANAGE/seeds/tweets.json", "r") as tweets_json:
    tweet_grab = json.load(tweets_json)
tweet = tweet_grab[0]    
print(tweet)



# for tweet in tweet_grab:
#     if tweet['location'] in clackamas_lat_long:
#         print(clackamas_lat_long[tweet['location']])    

timestamp = datetime.strptime(tweet['created_at'],
                     '%a %b %d %H:%M:%S +0000 %Y')
print(timestamp)



if tweet['coordinates'] != None:
    stated_coordinates = tweet['geo']['coordinates'] 
    coordinates.append(stated_coordinates)  
else:
    stated_coordinates = "No stated coordinated"
    coordinates.append(stated_coordinates)
    print("No stated coordinates")     
print(tweet['coordinates'])
 
if tweet['place'] != None:
    bounding_coordinates = tweet['place']['bounding_box']['coordinates'] 
    coordinates.append(bounding_coordinates) 
    print(bounding_coordinates)    
else:
    bounding_coordinates = "No bounding coordinates"
    coordinates.append(bounding_coordinates)
    print(bounding_coordinates)



#for tweet in tweet_grab:
tweet_dict = {'timestamp': timestamp, 'stated_coordinates': stated_coordinates,'bounding_coordinates':bounding_coordinates,}  
print(tweet_dict)               





#Unsure how to access Mogo Tweet database- onlist
# class TweetGrab:
#     def __init__(self, tweet_grab):
#         self.tweet_grab = tweet_grab

#     if not 'coordinates':'type' == 'point' 

#     if 'user':'location'== 'Clackamas County, Oregon'       
