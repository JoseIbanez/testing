#!/bin/bash

export POSTGRES_PASSWORD=$(pass develop/postgres/POSTGRES_PASSWORD)
export POSTGRES_USERNAME=$(pass develop/postgres/POSTGRES_USERNAME)
export POSTGRES_DB=demo
