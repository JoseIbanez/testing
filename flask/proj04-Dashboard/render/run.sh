#!/bin/sh
gunicorn --bind 0.0.0.0:8000 wsgi:app &
gunicorn --bind 0.0.0.0:8001 wsgi:app &
gunicorn --bind 0.0.0.0:8002 wsgi:app &
