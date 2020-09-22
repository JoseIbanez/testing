#!/bin/bash

PYTHONPATH=. luigi --module workflow MasterTask  --date=$1


#PYTHONPATH=. luigi --module workflow M100Task --workers 10

