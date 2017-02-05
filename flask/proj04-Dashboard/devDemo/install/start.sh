#!/bin/bash
op=`pwd`

source $op/../../docker/swarn112/env.sh

cd $op/../../render
screen -S render -d -m  ./run.sh

cd $op/../../kpi
screen -S kpi -d -m ./run.sh

cd $op/../../couter
screen -S counter -d -m  ./entrypoint.sh
