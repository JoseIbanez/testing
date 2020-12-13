from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import producer
import json

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

class VMDeployment(BaseModel):
    id: Optional[int] = None
    dc: str
    az: str
    rd: str
    os: str

class GenericTask(BaseModel):
    name: str
    delay: int
    value: str
    result: str

deployments = []

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.post("/deployments/vm/")
def create_vm(deployment: VMDeployment):
    """
    Create a VM deployment
    """
    id = len(deployments)
    
    item = deployment.dict()

    item["id"]=id
    deployments.append(item)
    return item

@app.get("/deployments/vm/{id}")
def get_vm(id: int):
    """
    Get a VM deployment
    """
    item=deployments[id]
    return item

@app.post("/task/")
def exe_genericTask(task: GenericTask):
    """
    Execute generic task
    """

    p1 = producer.MyProducter()


    item = task.dict()
    name = item.get("name")
    delay = item.get("delay")
    result = item.get("result")

    p1.publish(f"{name} running")
 
    print(f"delay: {delay}")
    time.sleep(delay)
 
    if result in ['error', 'fail']:
        p1.publish(f"{name} failed")
        raise HTTPException(status_code=503, detail=f"{name} error:{result}")
 
    p1.publish(f"{name} done")
    #p1.disconnect()
 
    return { name: result, "state": "done" }