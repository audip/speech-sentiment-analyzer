__author__ = 'saurabh'

#Import the necessary methods from tweepy library
import tweepy, json
import ConfigParser
from datetime import datetime, time
import pika


max_id = ""

class Tweet(object):
    def __init__(self, raw_tweet=None):
        self.text = raw_tweet.text
        self.created_by = raw_tweet.created_by
        self.id = raw_tweet.id_str
        self.retweet = raw_tweet.retweet_count


def load_config(self, service=None):
    """
    Reads the configuration from ini file
    @param service: service to which the API keys are required
    @return: dict of credentials for auth
    """
    Config = ConfigParser.ConfigParser()
    Config.read("sentiment_analyzer/config.ini")
    creds = {}

    if service == "Twitter":
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


def getTweets(searchTerm="MLH"):
    global max_id
    try:
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

            tweets = api.user_timeline(id=searchTerm, max_id=max_id, count=100)

            if tweets is None or tweets == []:
                print("Breaking from empty raw_tweets")
                break
            else:
                for tweet in tweets:
                    T = Tweet(tweet)

                    if most_recent_tweet is None:
                        most_recent_tweet = T.created_by

                    # Skip the last processed tweet
                    if max_id == T.id:
                        continue

                    message = "info: Hello World!"
                    channel.basic_publish(exchange='twitter_exchange', routing_key='', body=message,
                                          properties=pika.BasicProperties(delivery_mode=2))
                    print(" [x] Sent %r" % message)

                    max_id = T.id
                    api_calls += 1
    except Exception as e:
        print("Error in pulling twitter live stream data/n" + e)
    finally:
        connection.close()

def main():
    getTweets()

if __name__ == '__main__': # pragma: no cover
    main()