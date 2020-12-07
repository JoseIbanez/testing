from celery import Celery 
import time
from psql import deployGetState, deploySetState

broker = 'sqla+postgresql://flask:Password!@localhost/vc_deployments'
app = Celery(broker=broker)


@app.task(autoretry_for=(Exception,))
def wrk_deployment(deploymentId):


    print(f"DeploymentId {deploymentId}")
 
    state = deployGetState(deploymentId)
    state['state_summary'] = 'running'
    deploySetState(deploymentId, state)
    time.sleep(10)


    state = deployGetState(deploymentId)
    state['ip.state'] = 'done'
    state['state_summary'] = 'done'
    deploySetState(deploymentId, state)



    return 0

