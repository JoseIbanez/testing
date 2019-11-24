from celery import Celery

#app = Celery('t1.tasks1', backend='redis://localhost', broker='pyamqp://guest@localhost//')
app = Celery('t1.tasks1', backend='redis://redis', broker='pyamqp://guest@rabbitmq//')


@app.task
def add(x, y):
    return x + y

