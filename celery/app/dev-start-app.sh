#!/bin/bash

celery -A t1.tasks1 worker -n celery1@m1 --loglevel=info &
celery -A t2.tasks2 worker -n celery2@m1 --loglevel=info &

celery inspect registered

