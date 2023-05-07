import time
import random
import string
from rediscluster import RedisCluster


startup_nodes = [{"host": "redis-node", "port": "6379"},
                 {"host": "redis-cluster-redis-node-1", "port": "6379"},
                 {"host": "redis-cluster-redis-node-2", "port": "6379"}
                ]

rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)


counter = 0

while True:
    counter += 1
    key = ''.join(random.choices(string.ascii_uppercase, k=5))
    rc.set(key, f"{key}:{counter}")
    print(rc.get(key))
    time.sleep(.1)

