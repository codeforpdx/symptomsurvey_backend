#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 16:17:25 2018

@author: meganporter
"""
class DataStorage:
    def __init__(self, restaurant_name, key_words, count, date_range):
        self.restaurant_name = restaurant_name
        self.key_words = key_words
        self.count = count 
        self.date_range = date_range
        
    def get_restaurant_name(self):
        return self.restaurant_name
    def get_key_words(self):
        return self.key_words
    def get_count(self):
        return self.count
    def get_date_range(self):
        return self.date_range
    
    def set_restaurant_name(self, a_restaurant_name):
        self.restaurant_name = a_restaurant_name
    def set_key_words(self, key_words_list):
        self.key_words = key_words_list
    def set_count(self, new_count):
        self.count = new_count
    def set_date_range(self, select_range):
        self.date_range = select_range
        
        
    def harvest_key_words(self, word_harvest):
        sorted_list = []
        for word in word_harvest:
            if word in key_word_list:
                sorted_list.append(word)
    def machine_count(self, machine_data):
        """ Machine Learning Algorithm goes here
        So far K means seems like a good candidate but I'm only familiar with 
        K Means and K Nearest Neighbor.  I'm almost finished with algorithms, then
        I can go back to my machine learning class and investigate more options
        
        The goal of this algorithm would be to sort key_word data and classify 
        whether a given location can be classified as being the center of a 
        new Hepatitis A outbreat."""
        
    def when_key_words(self, select_range):
        """Search algorithm goes here.  I'm a few days away from working on the 
        search algorithm practice problems.  I'm starting the videos in the next
        two days."""



        """ list of key words, frequency count, baseline comparison frequency for alert purposes,
        list of key words is supposed to be asked about by someone at code for pdx for clackamas
        county.  look for symptoms before parsing or after? BEFORE. key words in addition to hashtags, 
        total number of tweets? GPS map?? WATCH VIDEOS ON DOCKER, some data analysis, convert csv's to usable
        database, still mongo??? Temporary database? python sqlite database-post on github Do we know
        if there is a time when the target population is more likely to tweet?  If so we can schedule
        the data harvest for that time?"""


        """make symptom list, frequency code, store in one csv, nltk code, filter for tweets coming 
        in 'store or not store?, percentage is num tweets/10000' 
       if #tweetswithsymptoms/#totaltweets > threshold, send alert
       Taking historical tweets by periods of time to build a csv database for Clackamas County.  Trend f
       frequency of keywords over time.  Barchart frequ of tweets by state by year.  Number of twitter users
       for normalization-........

       Fatigue
Sudden nausea, vomiting, throwing up, upchuck, spew, sick, so sick
Abdominal pain or discomfort, especially on the upper right side beneath your lower ribs (by your liver)
Clay-colored bowel movements, gray poop, gray feces, gray stool, off color poop, the shits, gray shit, holy shit!
Loss of appetite, not hungry, no appetite
Low-grade fever, ill, low fever, low temperature
Dark urine, what's wrong with my pee?, dark pee
Joint pain, arthritis?, hurting joints
Yellowing of the skin and the whites of your eyes (jaundice), yellow eyes, 
Intense itching, itchy, itchy!, scratching, 
        """

symptom_list = ['fatigue','sudden nausea','vomiting','throwing up','upchuck',
'spew','sick','so sick','abdominal pain','abdominal discomfort','painonrightside','liver pain', 
'clay colored bowel movements','gray poop', 'gray feces','gray stool','off color poop', 'the shits',
'gray shit', 'loss of appetite', 'not hungry', 'no appetite', 'low-grade fever', 'low fever', 'ill'
'low temperature','dark urine','what"s wrong with my pee?','dark pee','joint pain','hurting joints',
'yellowing of skin','yellow eyes','intense itching','itchy','scratching','jaundice']

# Ongoing concerns:
#ongoing storing of symptom heavy tweets in csv form and historical data
# for tweets, bar chart of most frequent symptom_list words? 
# what is the frequency for counter-alert system?  Will there be a counter alert system?
# What is the base threshold?
# num tweets/100000 or /total gets percentage 
# Wordclouds

# Look at tweets already harvested, lat long, clack county cities converted to lat and long
# reconcile github tweets with symptom list 

# write constructor and method for converting json object into usable data to search--> convert to 
# csv
# 
# 

clackamas_cities = ['Clackamas','Oregon City', 'Happy Valley','Milwaukie','West Linn','Canby',
'Estacada','Molalla','Canby', 'Gladstone','Boring', 'Damascus', 'Beaver Creek', 'Mulino', 'Oak Grove',
'Government Camp','Oatfield','Jennings Lodge','Johnson City','Stafford','Mount Hood Village', 'Barlow']

"""constructor, method for what goedata is present and what are we going to put in model, add 
timestamps, if there were responses or if tweet was a response to something else, 'If in reply status',
 something that produces a JSON copy of class"""

 # CMD SHIFT N Open new workspace