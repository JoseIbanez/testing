from celery import Celery 


broker = 'sqla+postgresql://flask:Password!@localhost/vc_deployments'

app = Celery(broker=broker)

@app.task
def add(x, y):
    return x + y


