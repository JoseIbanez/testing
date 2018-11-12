#!/usr/bin/env python

import time
import logging
import logging.handlers
import argparse
import sys
import socket


#Get options
parser = argparse.ArgumentParser(
         description='Send message to serial port')

parser.add_argument(
        '-port',
        type=str,
        help='serial port, eg. /tmp/channel0',
        default="/tmp/channel0")

parser.add_argument(
        '-msg',
        type=str,
        help='message to send, eg. 10;1010',
        default="10;1010")

parser.add_argument(
        '-wait',
        action='store_true',
        help='wait for 0')


args = parser.parse_args()


s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(args.port)
s.send(args.msg)
data = s.recv(1024)
s.close()
print('Received ' + repr(data))
