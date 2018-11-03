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