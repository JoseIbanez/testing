#!/bin/bash

PYTHONPATH=. luigi --module workflow MasterTask  --index=$1 --local-scheduler


#PYTHONPATH=. luigi --module workflow M100Task --workers 10

