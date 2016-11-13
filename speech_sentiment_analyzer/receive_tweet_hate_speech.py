#!/usr/bin/env python
import mq_library
from pymongo import MongoClient


def is_hate_speech(sentence):
    hate_words = set(['race','racism','discrimination','vandalism',
        'hate','slur','abuse','genocide','thug','thuggery','bigotry',
        'violence','sex','sexual', 'assault', 'bullying', 'shooting',
        'threat', 'threatening', 'kill', 'terror', 'terrorism', 'crime',
        'criminal', 'bashing', 'shaming', 'slut', 'abusive', 'nigga',
        'fuck', 'frick'
    ])
    for word in sentence:
        if word in hate_words:
            return True
    return False

def callback(ch, method, properties, body):
    # print("[x] %r" % body)

    client = MongoClient('mongodb://audip:audip@ds151917.mlab.com:51917/speech-db')

    body_split = body.split("::")
    text = body_split[0]

    tweet = mq_library.preprocess_text(text)

    # Save to mongodb
    db = client['speech-db']
    hate_speech = db['speech-feed']

    senti, score = mq_library.get_sentiment_textblob(tweet)
    tweet_str = ' '.join(s for s in tweet)

    tweet_post = {'text':tweet_str,'id':body_split[1],
    'retweet':body_split[2],'created_at':body_split[3],
    'sentiment': senti, 'score': score}

    if not is_hate_speech(tweet):
        tweet_post["hate"]='false'
    else:
        tweet_post["hate"]='true'

    speech = db.hate_speech
    speech.insert_one(tweet_post)

    ch.basic_ack(delivery_tag = method.delivery_tag)

def main():

    channel = mq_library.setup_messaging_queue()
    print('[*] Waiting for logs. To exit press CTRL+C')
    channel.basic_consume(callback, queue='twitter_mq')

    channel.start_consuming()

if __name__ == '__main__':
    main()
