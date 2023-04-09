#!/bin/bash

export ACELINKHOST="$(hostname -I | cut -d ' ' -f 1)"
export TELEGRAM_BOT_TOKEN=`pass telegram/BOTLICHE_TOKEN`
docker-compose up -d

