#!/bin/bash

cat /var/log/system.log |   websocat -H="X-Auth-Token: aa"  "ws://127.0.0.1:8000/items/33/ws" | pv
