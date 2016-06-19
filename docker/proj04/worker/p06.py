#!/usr/bin/python

import redis
import time
from uuid import getnode as get_mac

mac=hex(get_mac())
r_server = redis.Redis("redis")
r_server.sadd("workers","worker:"+mac)

while True:
    c=r_server.incr("hit_counter")
    wc=r_server.hincrby("worker:"+mac,"hit",1)
    r_server.expire("worker:"+mac,10)
    print "all",c
    print mac,wc

    for w in r_server.smembers("workers"):
        wc=r_server.hget(w,"hit")
        if (wc is None):
            r_server.srem("workers",w)
            continue
        print w,wc

    time.sleep(1)
