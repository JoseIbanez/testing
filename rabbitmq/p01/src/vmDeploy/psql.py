#!/usr/bin/env python
import psycopg2
from psycopg2.extras import RealDictCursor
import json


def deployGetState(deploymentId):

    querySelect = """
    SELECT state,state_summary
    FROM deployments
    WHERE id = %s
    LIMIT 1
    """

    db = DeploymentDB()
    print(f"Select DeploymentId {deploymentId}")
    resultDB=db.execute(querySelect, [deploymentId,])
    db.disconnect()

    try:
        state = json.loads(resultDB[0]["state"])
    except:
        state = {}
    #print(state)
    state['state_summary'] = resultDB[0]["state_summary"]


    return state



def deploySetState(deploymentId,state):
    queryUpdate = """
    UPDATE deployments
    SET 
        state = %s,
        state_summary = %s
    WHERE id = %s
    """


    db = DeploymentDB()
    print(f"Update DeploymentId {deploymentId}")
    db.update(queryUpdate, [json.dumps(state), state['state_summary'], deploymentId,])
    db.disconnect()

    return 0



class DeploymentDB(object):

    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = psycopg2.connect(user = "flask",
                                  password = "Password!",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "vc_deployments")

        # Print PostgreSQL Connection properties
        #print ( self.connection.get_dsn_parameters(),"\n")
        #print("PSQL: Connected")


    def select(self,query,params):

        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        # Print PostgreSQL version
        cursor.execute(query,params)
        #record = cursor.fetchone()
        #print("Result ", record,"\n")
        result = cursor.fetchall()
        print("Result ", json.dumps(result),"\n")

        cursor.close()
        return result


    def update(self,query,params):
        cursor = self.connection.cursor()
        cursor.execute(query,params)
        self.connection.commit()
        cursor.close()
        return 0


    def execute(self,query,params):
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query,params)
        result = cursor.fetchall()
        cursor.close()
        return result


    def disconnect(self):
        if(self.connection):
            self.connection.close()
            #print("PSQL: closed")

if __name__ == "__main__":

    db = DeploymentDB()
    db.select("SELECT version();",None)
    db.select("SELECT * from deployments where type = %s;",["demo"])
    db.update("""
    INSERT into deployments 
    (type,request,state,state_summary)
    values 
    ('demo','','','new');
    """, None)
    db.disconnect()

    state = deployGetState(1)
    state['state_summary'] = 'new'
    deploySetState(1, state)