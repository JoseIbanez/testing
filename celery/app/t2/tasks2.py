from celery import Celery

#app = Celery('t2.tasks2', backend='redis://localhost', broker='pyamqp://guest@localhost//')
app = Celery('t2.tasks2', backend='redis://redis', broker='pyamqp://guest@rabbitmq//')

@app.task
def rest(x, y):
    return x - y

