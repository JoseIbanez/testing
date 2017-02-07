#!/bin/bash

eval "$(cat mysql.env | sed 's/^/export /')"
