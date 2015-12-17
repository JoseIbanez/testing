#!/bin/sh
git pull
gunicorn --bind 0.0.0.0:8000 wsgi

