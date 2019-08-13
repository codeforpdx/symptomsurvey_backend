from services import database_service


def get_tweets_from_db(search_text=None, limit=100):
    """ Retrieve Tweets from Database. """
    mongo = database_service.get_mongo_client()
    matching_tweets = mongo.db.tweets.find(
        format_db_search(search_text)
    ).sort('id', -1).limit(limit)
    return list(matching_tweets)


def format_db_search(search_text):
    if search_text is not None:
        return {'$text': {'$search': search_text}}
    else:
        return {}
