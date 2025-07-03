#!/bin/bash

export PREFECT_API_URL="http://127.0.0.1:4200/api"

prefect worker start --pool "Local"
