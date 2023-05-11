import time
import random
import string
import os
from rediscluster import RedisCluster
from redis import Redis

REDIS_N1 = os.environ.get("REDIS_NODE1")
REDIS_P1 = os.environ.get("REDIS_PORT1","6379")



startup_nodes = [{"host": REDIS_N1, "port": REDIS_P1}]

rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
print(rc)
#rs = Redis(host='localhost', port=6379, decode_responses=True)
rs = rc


counter = 0

task_list = ["t1","t2","t3","t4","t5"]

while True:
    counter += 1
    key = ''.join(random.choices(string.ascii_uppercase, k=5))

    rc.set(key, f"{key}:{counter}",ex=30)

    print(rc.get(key))
    time.sleep(.1)


    for task in task_list:

        lock = rc.lock(task,timeout=10)
        if lock.acquire(blocking=False):
            print(f"running {task}")
            time.sleep(4)
            break




