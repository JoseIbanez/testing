#!/usr/bin/python

import redis
import time

with open("redis.lst","r") as f:
  content=f.read().splitlines()
f.close()


r_server = redis.Redis(content[0])
r_server.set("name", "DeGizmo")
n=r_server.get("name")

while True:
    r_server.incr("hit_counter")
    c=r_server.get("hit_counter")

    print n
    print c

    time.sleep(1)
