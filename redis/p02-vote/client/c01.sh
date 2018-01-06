#!/bin/bash

curl http://redis:8000/
echo


curl http://redis:8000/v1/vote?color=red
echo
curl http://redis:8000/v1/vote?color=blue
echo

curl http://redis:8000/v1/listVotes
echo
curl http://redis:8000/v1/listWorkers
echo

