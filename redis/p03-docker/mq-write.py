#!/usr/bin/env python
import pika
import time


credentials = pika.credentials.PlainCredentials("writer", "writer", erase_on_connect=False)


connection = pika.BlockingConnection(pika.ConnectionParameters(credentials=credentials, host='rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='hello')

#time
itime = int(round(time.time() * 1000))

i = 10000000
while i > 0:
    #time.sleep(0.01)
    i = i - 1

    channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!'+str(i))


print(" [x] Sent 'Hello World!'")


connection.close()

#time
ftime = int(round(time.time() * 1000))
print ftime-itime
