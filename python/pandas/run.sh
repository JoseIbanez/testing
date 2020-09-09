#!/bin/bash

PYTHONPATH=. luigi --module workflow MasterTask  --index=$1
