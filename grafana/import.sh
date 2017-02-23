#!/bin/bash

curl -i -XPOST 'http://localhost:8086/write?db=mydb' --data-binary @$1
