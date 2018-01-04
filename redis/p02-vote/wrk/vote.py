#!/usr/bin/python
import collections
import os
import time
from uuid import getnode as get_mac
import redis
from flask import Flask, json, request

app = Flask(__name__)
cuenta = 0

#Connect to redis server
r_server = redis.Redis("redis")

#add worker id to SET
worker_id = hex(get_mac())
#worker_id = hex(get_mac())+"."+str(os.getpid())
r_server.sadd("workers", "worker:"+ worker_id )



@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/v1/vote', methods=['GET', 'POST'])
def vote():

    color = request.args.get('color')

    # Add vote color to SET
    r_server.sadd("votes", "vote:"+color)

    # Increase counters
    c = r_server.incr("hit_counter")
    vc = r_server.hincrby("vote:" + color, "hit", 1)
    wc = r_server.hincrby("worker:" + worker_id, "hit", 1)
    
    # Refresh server/vote presence
    r_server.expire("worker:" + worker_id, 500)
    r_server.expire("vote:" + color, 500)


    # Prepare answer
    oList = []
    d = collections.OrderedDict()
    d['color:' + color] = vc
    d['worker:' + worker_id] = wc
    oList.append(d)


    return json.dumps(oList)


@app.route('/v1/listWorkers')
def listWorkers():
    oList = []
    for w in r_server.smembers("workers"):
        wc = r_server.hget(w, "hit")
        if wc is None:
            r_server.srem("workers", w)
            continue

        d = collections.OrderedDict()
        d[w] = wc
        oList.append(d)

    return json.dumps(oList)


@app.route('/v1/listVotes')
def listVotes():
    oList = []
    for v in r_server.smembers("votes"):
        vc = r_server.hget(v, "hit")
        if vc is None:
            r_server.srem("votes", v)
            continue

        d = collections.OrderedDict()
        d[v] = vc
        oList.append(d)

    return json.dumps(oList)



if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
