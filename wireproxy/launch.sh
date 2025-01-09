#!/bin/bash

CONFIG_PATH=~/.config/wireproxy
CONFIG_FILE="$CONFIG_PATH/proton-vpn.conf"

# Check if the file exists
if [ -f $CONFIG_FILE ]; then
    echo "Config file: $CONFIG_FILE exists."
else
    echo "Config file: $CONFIG_FILE does not exist."
    mkdir -p $CONFIG_PATH
    pass wireproxy/proton-vpn > $CONFIG_FILE
fi

# Start the WireProxy client
wireproxy -c $CONFIG_FILE
rm $CONFIG_FILE



