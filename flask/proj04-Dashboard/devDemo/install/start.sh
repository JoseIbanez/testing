#!/bin/bash
op=`pwd`

source ./env.sh

cd $op/../../render
screen -S render -d -m  ./run.sh

cd $op/../../kpi
screen -S kpi -d -m ./run.sh

cd $op/../../counter
screen -S counter -d -m  ./entrypoint.sh
