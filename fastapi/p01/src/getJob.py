#!/usr/bin/env python
from psql import DeploymentDB
import json
import sys

def getJob(type):

    query = """
    SELECT *
    FROM deployments
    WHERE type = %s
          and state_summary = 'new'
    LIMIT 1
    """

    db = DeploymentDB()
    result = db.execute(query, [type,] )
    db.disconnect()
    print(json.dumps(result))

    return 0




if __name__ == "__main__":


    type = sys.argv[1]

    getJob(type)

