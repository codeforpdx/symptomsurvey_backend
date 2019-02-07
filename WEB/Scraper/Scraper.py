from twitterscraper import query_tweets
import datetime as dt

if __name__ == '__main__':
    data = query_tweets("state of the union", limit=10, begindate=dt.date(2018, 12, 20)) #limit is 10 tweets here

with open("data.txt", mode='w') as file: # Use file to refer to the file object
    for tweet in data[:10]: #at least 10 results within the minimal possible time/number of requests
        print(tweet.text.encode('utf-8'))
        file.write(str(tweet.text.encode('utf-8'))+'\n')
