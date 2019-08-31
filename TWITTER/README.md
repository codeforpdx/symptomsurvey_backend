TWITTER Service
===============

Periodically retrieve recent tweets and record them to database.

Provides a simple web interface at :5001 (by default) for status.

Note:
FLASK has a nice "reload" feature that restarts the server if you change
source code.  However, it doesn't kill the process, so the "cron" events
are duplicated resulting in duplicate tweets written to the db.

Conceptual Overview
-------------------
We want to periodically talk to the Twitter API and ask for new tweets that
are in the vacinity.  Those tweets are retrieved and then written to a mongo
database.

This is done with a single program consisting of a twitter grabber and a mongodb
writer.  They communicate through a shared in-memory queue.

File Layout
-----------
app.py - The main Flask app, which:
    Reads the ../SHARED/constants.json file for parameters
    Creates a queue.Queue() for communication
    Starts the mongo manager which triggers every 12 seconds
    Starts the twitter manager which triggers every
        settings['get_interval_in_seconds']
    Provides a very simple web page showing the last tweet and mongodb status
twitter.py - Code which retrieves tweets from the twitter API
    Provides TwitterReader() class, which:
        .get_tweets() is called periodically.
        .get_tweets() connects to Twitter and iterates until it retrives all
            the tweets that are available.
            writes tweets to the Queue
mongo.py - Code which manages mongo database.
    Provides MongoWriter() class, which:
        Periodically checks Queue for new Tweets.
        Writes any new tweets to mongo db
        processes requests for mongodb

Handy mongodb operations
------------------------
* Enter the docker container:
docker exec -it sms-mongodb bash
* Start mongo command line:
mongo
* List all the databases:
show dbs
* Select one for use
use <new_dbs>
* List all the collections inside the database
show collections
* List all the rows of the collection and the number of rows
db.<collection>.find({})
db.<collection>.count()

- How many records are in our raw_tweets database?
use raw_tweets
db.tweets.count()
