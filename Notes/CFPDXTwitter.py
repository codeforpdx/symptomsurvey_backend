#Assuming that tweets have already been harvested and stored in a CSV.
# I used Tweepy and Textblob but it looks like we are using something different.




"""Using a symptom list for tweet harvesting"""

symptom_tweets = api.search(['fatigue','sudden nausea','vomiting','throwing up','upchuck',
'spew','sick','so sick','abdominal pain','abdominal discomfort','painonrightside','liver pain', 
'clay colored bowel movements','gray poop', 'gray feces','gray stool','off color poop', 'the shits',
'gray shit', 'loss of appetite', 'not hungry', 'no appetite', 'low-grade fever', 'low fever', 'ill'
'low temperature','dark urine','what"s wrong with my pee?','dark pee','joint pain','hurting joints',
'yellowing of skin','yellow eyes','intense itching','itchy','scratching','jaundice'])

# Simple code from Siraj Rival for basic sentiment analysis
import tweepy
from textblob import TextBlob

for tweet in symptom_tweets:
    
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    print()

"""Tokenizing Tweets"""

import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

#df['Tweet'] is a placeholder
for tweet in df['Tweet']:
    token = word_tokenize(tweet)
    print(token)


# Tweets according the symptom list

filtered_words = []
for tweet in df['Tweet']:
    token = word_tokenize(tweet)
    for item in token:
        if item in symptom_tweets:
            filtered_words.append(item)    
counts = Counter(filtered_words)
print(counts)


"""Visualization"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import operator

d_counts = dict(counts)
sorted_d_counts = sorted(d_counts.items(), key=operator.itemgetter(1),reverse=True)
print(sorted_d_counts)

"""Convert list of tuples to list of lists to consolidate data"""
sorted_counts = [list(x) for x in sorted_d_counts]
print(sorted_counts)

print(sorted_counts[:10])

"""Convert back to list of tuples for graphing"""
tuple_list = [tuple(x) for x in sorted_counts]
print(tuple_list)


"""Code to be modified for actual tweet harvest"""
# plt.bar(range(len(limit_counts)), [val[1] for val in limit_counts], align='center')
# plt.rcParams["figure.figsize"] = (20,20)
# plt.xlabel('Symptom')
# plt.ylabel('Frequency')
# plt.title('Most Common Symptoms Associated with Symptom List')
# plt.xticks(range(len(limit_counts)), [val[0] for val in limit_counts])
# plt.xticks(rotation=70)
# plt.show()


