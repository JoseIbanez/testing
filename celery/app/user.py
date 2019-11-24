#!/usr/bin/python3

from t1.tasks1 import add
from t2.tasks2 import rest
import time

r1 = add.delay(4, 4)
r2 = rest.delay(4, 1)


while (not r1.ready() or not r2.ready() ):
    time.sleep(1)
    print("r1 "+str(r1.ready()))
    print("r2 "+str(r2.ready()))

print(r1.result)
print(r2.result)
