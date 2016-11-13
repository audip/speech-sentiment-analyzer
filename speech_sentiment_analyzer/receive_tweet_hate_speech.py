#!/usr/bin/env python
import mq_library


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
            print("True")
            return True
    print("false")
    return False

def callback(ch, method, properties, body):
    print("[x] %r" % body)

    tweet = mq_library.preprocess_text(body)
    if not is_hate_speech(tweet):
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return

    # Save to mongodb

    ch.basic_ack(delivery_tag = method.delivery_tag)

channel, queue_name = mq_library.setup_messaging_queue()
print('[*] Waiting for logs. To exit press CTRL+C')
channel.basic_consume(callback, queue=queue_name)

channel.start_consuming()
