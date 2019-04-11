#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 16:17:25 2018

@author: meganporter
"""
class DataStorage:
    def __init__(self, date, time, text, hashtags, web_address):
        self.date = date
        self.time = time
        self.text = text 
        self.hashtags = hashtags
        self.web_address = web_address
        
    def get_date(self):
        return self.date
    def get_time(self):
        return self.time
    def get_text(self):
        return self.text
    def get_hashtags(self):
        return self.hashtags
    def get_web_address(self):
        return self.web_address    
    
    def set_date(self, a_date):
        self.date = tweet_date
    def set_time(self, time_list):
        self.time = tweet_time
    def set_text(self, new_text):
        self.text = tweet_text
    def set_hashtags(self, select_range):
        self.hashtags = tweet_hashtags
    def set_web_address = a_web_address    
        
        
    def harvest_time(self, word_harvest):
        sorted_list = []
        for word in word_harvest:
            if word in key_word_list:
                sorted_list.append(word)
    def machine_text(self, machine_data):
        """ Machine Learning Algorithm goes here
        Do we need this?"""
        
    def when_time(self, select_range):
        """Search algorithm goes here.  Do we need this?"""