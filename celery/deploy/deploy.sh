#!/bin/bash


apt install -y docker.io python3-pip docker-compose

umask 022
pip3 install Celery redis

