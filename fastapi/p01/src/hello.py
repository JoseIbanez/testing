#!/usr/bin/env python

import asyncio
import time
import producer
import json

p1 = producer.MyProducter()


async def fun1(a,b,result):
    p1.publish("fun1. running")
    await asyncio.sleep(2)
    result["c"] = a+b
    #print(f"fun1 {c}")
    p1.publish("fun1. done")
    p1.publish(json.dumps(result))


async def fun2(a,b,result):
    p1.publish("fun2. running")
    await asyncio.sleep(1)
    result["d"] = a-b
    #print(f"fun2 {c}")
    p1.publish("fun2. done")
    p1.publish(json.dumps(result))


async def funGen(name,time,value,result):

    if result.get(name+".state") == "done":
        return

    p1.publish(f"{name} running")
    result[name+".state"] = "running"
    await asyncio.sleep(time)
    result[name] = value
    result[name+".state"] = "done"
    p1.publish(f"{name} done")
    p1.publish(json.dumps(result))


async def deploy(deployment):

    result = deployment

    tasks = []
    tasks.append(funGen("name",1,"es000yr",result))
    tasks.append(funGen("ipFE",1,"44.44.44.10",result))
    tasks.append(funGen("ipMG",1,"10.10.10.10",result))
    await asyncio.wait(tasks)

    tasks = []
    tasks.append(funGen("Clone",10,"done",result))
    tasks.append(funGen("Infoblox",1,"done",result))
    await asyncio.wait(tasks)

    tasks = []
    tasks.append(funGen("Route",2,"done",result))
    tasks.append(funGen("Locale",2,"done",result))
    tasks.append(funGen("Avamar",2,"done",result))
    tasks.append(funGen("Zerto",2,"done",result))
    await asyncio.wait(tasks)





async def main():
    result1 = { "id":1 }
    result2 = { "id":2 }

    await deploy(result1)
    await deploy(result2)
    await deploy(result1)




if __name__ == "__main__":
    s = time.perf_counter()

    asyncio.run(main())

    elapsed = time.perf_counter() - s
    print(f"Execution time: {elapsed:0.2f} seconds.")


