#!/bin/sh
gunicorn --bind 0.0.0.0:8012 wsgi:app
