#!/bin/bash

PYTHONPATH=. luigi --module workflow MasterTask  --index=$1


#PYTHONPATH=. luigi --module workflow M100Task
