#!/usr/bin/env python
import mq_library

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    tweet = mq_library.preprocess_text(body)
    sentiment, score = mq_library.get_sentiment_textblob(tweet)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel, queue_name = mq_library.setup_messaging_queue()
print(' [*] Waiting for logs. To exit press CTRL+C')
channel.basic_consume(callback, queue=queue_name)

channel.start_consuming()
