#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import functools
import logging
import time
import pika
import sys

LOGGER = logging.getLogger(__name__)


class MyProducter(object):

    def __init__(self, host="localhost", exchange="logs" ):
        self.host = host
        self.exchange = exchange
        self.connection = None
        self.channel = None

        self.connect()


    def connect(self):
        self.connection = pika.BlockingConnection(
                                pika.ConnectionParameters(host=self.host))

        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange, exchange_type='fanout')


    def disconnect(self):
        self.connection.close()


    def publish(self,message):
        self.channel.basic_publish(exchange=self.exchange, routing_key='', body=message)
        print(" [x] Sent %r" % message)


if __name__ == '__main__':
    
    message = ' '.join(sys.argv[1:]) or "info: Hello World!"

    mypr = MyProducter()
    mypr.publish(message)
    mypr.disconnect()