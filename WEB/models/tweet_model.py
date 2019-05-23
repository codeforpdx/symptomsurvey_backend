

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
            'Stafford':[45.357342,-122.722595],'Barlow':[45.252257,-122.721223],
        }

        #save as string, no conversion necessary
        timestamp = tweet['created_at']
        # datetime.strptime ,
        #             '%a %b %d %H:%M:%S +0000 %Y')
        # if tweet['location'] in clackamas_lat_long:
        #     city_coordinates = clackamas_lat_long[tweet['location']]
        # else:
        #     city_coordinates = "No Clackamas city coordinates"

        if tweet['user']['location'] in clackamas_lat_long:
            user_coordinates = clackamas_lat_long[tweet['user']['location']]
        else:
            user_coordinates = "No user coordinates"                 


        if tweet['coordinates'] != None:
            stated_coordinates = tweet['geo']['coordinates']   
        else:
            stated_coordinates = "No stated coordinated"


        if tweet['place'] != None:
            bounding_coordinates = tweet['place']['bounding_box']['coordinates']      
        else:
            bounding_coordinates = "No bounding coordinates"

        tweet_info = {'timestamp': timestamp, 'user_coordinates':user_coordinates,'stated_coordinates':stated_coordinates,'bounding_coordinates':bounding_coordinates,} 
#'city_coordinates':city_coordinates,
        #Convert back into JSON
        with open("data_file.json", "w") as write_file:
            json.dump(tweet_info, write_file)


