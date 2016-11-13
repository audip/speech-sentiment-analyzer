#!/usr/bin/env python
import mq_library, json


def callback(ch, method, properties, body):
    print(" [x] %r" % body)

    try:
        body_split = body.split("::")
        text = body_split[0]

        tweet = mq_library.preprocess_text(text)
        sentiment, score = mq_library.get_sentiment_textblob(tweet)
        ch.basic_ack(delivery_tag = method.delivery_tag)
    except UnicodeDecodeError as e:
        pass

channel, queue_name = mq_library.setup_messaging_queue()
print(' [*] Waiting for logs. To exit press CTRL+C')
channel.basic_consume(callback, queue=queue_name)

channel.start_consuming()
