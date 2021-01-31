#!/usr/bin/env python
from psql import DeploymentDB
import json
import sys
import time

from deployments import wrk_deployment


def post_deployment(type,request,requestor):

    queryInsert = """
    INSERT INTO deployments
    (type,request,state,state_summary)
    VALUES
    (%s,%s,'','new')
    RETURNING id;
    """

    queryUpdate = """
    UPDATE deployments
    SET taskId = %s
    WHERE id = %s
    """


    db = DeploymentDB()
    dbResult = db.execute(queryInsert, [type, json.dumps(request)])
    deploymentId = dbResult[0]["id"]

    task = wrk_deployment.delay(deploymentId)
    dbResult = db.update(queryUpdate, [task.id, deploymentId])

    db.disconnect()

    result = { "id": deploymentId, "taskId": task.id }
    #print(result)


    return result, 200




if __name__ == "__main__":

    request = sys.stdin.read()
    url = sys.argv[1]

    requestJson = json.loads(request)
    type = requestJson.get("type")
    #request = {"type": "demo", "az":"RAT-AZ1", "os":"RHEL8"}
    #type = request["type"]
    requestor = "console"
    result, code  = post_deployment(type,requestJson,requestor)
    print(json.dumps(result), code)

