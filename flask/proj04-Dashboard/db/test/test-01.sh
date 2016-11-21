#!/bin/bash

mysql \
 --defaults-file=./my.cnf \
 bdb \
 -e "source test-01.sql;"
