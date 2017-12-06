#!/usr/bin/env python
import pika
import time


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

#time
itime = int(round(time.time() * 1000))

for i in range(0, 100000):

    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!'+str(i))


print(" [x] Sent 'Hello World!'")


connection.close()

#time
ftime = int(round(time.time() * 1000))
print ftime-itime
