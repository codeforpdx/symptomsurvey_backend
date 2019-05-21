"""Removing obvious noise"""

# All the extra characters in harvested tweets don't look the same as the HTML code I am trying to remove
# from a CSV in another project.  Creating a list of known nonsense strings is the only thing I could come 
# up with to clean the tweets a little bit.  Any suggestions are welcome.

# del_list = ['b', "''", "'", '@', "''", "b'RT", 's\\\\xe2\\\\x80\\\\xa6',"b'b"]
# for tweet in df['Tweet']:
#     token = word_tokenize(tweet)
#     for item in token:
#         for char in del_list:
#             if char in token:
#                 token.remove(char)
#     print(token) 

#     """Word counts by tweet"""
# from collections import Counter
# del_list = ['b', "''", "'", '@', "''", "b'RT","b'b",'#', ":",'https',',',';','!',
#                 '.',"'s",'$','-','&']
# for tweet in df['Tweet']:
#     token = word_tokenize(tweet)
#     for item in token:
#         for char in del_list:
#             if char in token:
#                 token.remove(char)
#     counts = Counter(token)
#     print(counts)   

"""First attempt at single list"""
word_list = []
from collections import Counter
del_list = ['b', "''", "'", '@', "''", "b'RT","b'b", "#", ":",'https',',',';','!',
                '.',"'s",'$','-','&']
for tweet in df['Tweet']:
    token = word_tokenize(tweet)
    for item in token:
        for char in del_list:
            if char in token:
                token.remove(char)
    for item in token:
        word_list.append(item)
        
"""Print Counts"""

counts = Counter(word_list)
print(counts)  

"""Download StopWords"""
nltk.download('stopwords')

"""Remove Stopwords in addition to repeating noise
   Print clean, individual tweets"""
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))

for tweet in df['Tweet']:
    token = word_tokenize(tweet)
    filtered_words = []
    del_list = ['b', "''", "'", '@', "''", "b'RT", 's\\\\xe2\\\\x80\\\\xa6',"b'b", '#', ":"]
    for item in token:
        for char in del_list:
            if char in token:
                token.remove(char)
    for item in token:
        if item not in stopWords:
            filtered_words.append(item) 
    
    print(filtered_words)


    """Print final list"""
filtered_words = []
for tweet in df['Tweet']:
    token = word_tokenize(tweet)
    del_list = ['b', "''", "'", '@', "''", "b'RT", 's\\\\xe2\\\\x80\\\\xa6',"b'b", '#', ":",'https',',',';','!',
                '.',"'s",'$','-','&']
    for item in token:
        for char in del_list:
            if char in token:
                token.remove(char)
    for item in token:
        if item not in stopWords:
            filtered_words.append(item) 
    
counts = Counter(filtered_words)
print(counts)
