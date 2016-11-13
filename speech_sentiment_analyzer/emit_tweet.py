#!/usr/bin/env python
import pika
import sys

def setup_messaging_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='twitter_exchange',type='fanout')
    channel.basic_publish(exchange='twitter_exchange',routing_key='',body=message, properties=pika.BasicProperties(delivery_mode=2))

    return channel, connection

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel, connection = setup_messaging_queue()
print(" [x] Sent %r" % message)

connection.close()
