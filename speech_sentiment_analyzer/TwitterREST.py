__author__ = 'saurabh'

#Import the necessary methods from tweepy library
import tweepy, json
import ConfigParser
from datetime import datetime, time
import pika
import time


max_id = ""

class Tweet(object):
    def __init__(self, raw_tweet=None):
        self.text = raw_tweet.text
        self.created_at = raw_tweet.created_at
        self.id = raw_tweet.id_str
        self.retweet = str(raw_tweet.retweet_count)

    def getJSON(self):
        tweet = {
            'text': self.text,
            'created_at': self.created_at,
            'id': self.id,
            'retweet_count': self.retweet
        }

        return tweet

def load_config(service="Twitter"):
    """
    Reads the configuration from ini file
    @param service: service to which the API keys are required
    @return: dict of credentials for auth
    """
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    creds = {}

    creds["key"] = Config.get("TwitterAuth", "key")
    creds["secret"] = Config.get("TwitterAuth", "secret")
    creds["token"] = Config.get("TwitterAuth", "token")
    creds["token_secret"] = Config.get("TwitterAuth", "token_secret")
    return creds if creds != {} else None


def setupTwitterConnection():
    creds = load_config()
    try:
        consumer_key = creds["key"]
        consumer_secret = creds["secret"]
        access_token = creds["token"]
        access_token_secret = creds["token_secret"]

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return tweepy.API(auth)
    except:
        print("Unable to establish connection to twitter API!!!\n")
        print("Please check internet connectivity")


def pause_processing(start_time, minutes=16):
    time_gap = 60*minutes
    end_time = datetime.now()
    difference = end_time - start_time
    delta = difference.seconds
    print("Program sleeping for %s mins after %s" % (minutes, start_time))
    time.sleep(time_gap - delta)


def setup_messaging_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='twitter_exchange',type='fanout')
    return channel, connection


def getTweets(searchTerm="MLHacks"):
    global max_id
    # try:
    start_time = datetime.now()
    print("Start time of run %s " % str(start_time))

    api = setupTwitterConnection()
    channel, connection = setup_messaging_queue()
    api_calls = 1
    most_recent_tweet = None

    while True:
        if api_calls > 175:
            pause_processing(start_time, minutes=16)
            api_calls = 1
            start_time = datetime.now()

        if max_id == "":
            tweets = api.user_timeline(id=searchTerm, count=100)
        else:
            tweets = api.user_timeline(id=searchTerm, max_id=max_id, count=100)

        if tweets is None or tweets == []:
            print("Breaking from empty raw_tweets")
            break

        for tweet in tweets:
            T = Tweet(tweet)

            if most_recent_tweet is None:
                most_recent_tweet = T.created_at

            # Skip the last processed tweet
            if max_id == T.id:
                continue

            # message = json.dumps(T.getJSON())
            message = T.text+'::'+T.id+'::'+T.retweet+'::'+str(T.created_at)
            channel.basic_publish(exchange='twitter_exchange', routing_key='', body=message,
                                  properties=pika.BasicProperties(delivery_mode=2))
            print(" [x] Sent %r" % message)

            max_id = T.id

        api_calls += 1

    connection.close()
    # except Exception as e:
        # print(e)

def main():
    getTweets()

if __name__ == '__main__': # pragma: no cover
    main()
