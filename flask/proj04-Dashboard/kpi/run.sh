#!/bin/sh
gunicorn --bind 0.0.0.0:8010 wsgi:app

