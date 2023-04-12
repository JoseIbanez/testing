#!/bin/bash

bw_search () {
    bw list items --search $1 | jq -r '.[].name'
}

bw_field () {
    bw get item $1 | jq -r " .fields[] | select(.name==\"$2\") | .value "
}

bw_folders () {
    bw list folders --search $1 | jq -r '.[].name'
}

jq_field () {
    FIELD=$1
    echo $ITEM | jq -r ".fields[] | select(.name==\"$FIELD\") | .value"
}

bw_item () {
    FOLDER=$1
    NAME=$2
    FOLDER_ID=$(bw get folder $FOLDER | jq -r '.id')
    bw list items --search $NAME --folderid $FOLDER_ID | jq -c -r '.[0]'
}



ITEM=$(bw_item "rn/preprod" "ElasticSearch.prerpod")
echo $(echo $ITEM | jq -r '.login.username' )
echo $(echo $ITEM | jq -r '.login.password' )
APM_KEY=$(jq_field APM_KEY)
echo $APM_KEY

