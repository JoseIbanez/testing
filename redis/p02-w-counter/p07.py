#!/usr/bin/python
import redis
import time
from uuid import getnode as get_mac
from flask import Flask, json, request
import collections

app = Flask(__name__)
cuenta=0

#Connect to redis server
with open("redis.lst","r") as f:
    content=f.read().splitlines()
f.close()
r_server = redis.Redis(content[0])

#register worker
mac=hex(get_mac())
r_server.sadd("workers","worker:"+mac)



@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/v1/vote', methods=['GET', 'POST'])
def vote():

    color= request.args.get('color')
    vc=r_server.hincrby("vote:"+color,"hit",1)

    c=r_server.incr("hit_counter")
    wc=r_server.hincrby("worker:"+mac,"hit",1)
    r_server.expire("worker:"+mac,500)

    oList=[]
    d = collections.OrderedDict()
    d['color:'+color]=vc
    d['worker:'+mac]=wc
    oList.append(d)

    return json.dumps(oList)


@app.route('/v1/listWorkers')
def query():
    oList=[]
    for w in r_server.smembers("workers"):
        wc=r_server.hget(w,"hit")
        if (wc is None):
            r_server.srem("workers",w)
            continue

        d = collections.OrderedDict()
        d[w]=wc
        oList.append(d)

    return json.dumps(oList)

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
