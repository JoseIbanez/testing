#!/usr/bin/env python
import pika
import asyncio
import time

async def firstWorker():
    while True:
        await asyncio.sleep(1)
        print("First Worker Executed")

async def secondWorker():
    while True:
        await asyncio.sleep(5)
        print("Second Worker Executed")

async def consumer01():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name)

    print('[C1] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print("[C1] %r" % body)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()



async def consumer02():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name)
    print('[C2] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print("[C2] %r" % body)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()





loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(firstWorker())
    asyncio.ensure_future(secondWorker())
    #asyncio.ensure_future(consumer01())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
