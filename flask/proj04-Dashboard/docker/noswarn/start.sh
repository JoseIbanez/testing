#!/bin/sh


docker run -d --name bdb_kpi \
	--env-file ./mysql.env \
	ibanez/bdb_kpi

docker run -d --name bdb_render \
	--env-file ./mysql.env \
	ibanez/bdb_render

