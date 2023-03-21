#!/bin/bash

bw_search () {
    bw list items --search $1 | jq -r '.[].name'
}


bw_field () {
    bw get item $1 | jq -r " .fields[] | select(.name==\"$2\") | .value "
}

