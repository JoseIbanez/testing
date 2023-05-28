#!/bin/bash

export SRC_DIR=../protos
export DST_DIR=../collector


python -m grpc_tools.protoc -I=$SRC_DIR --python_out=$DST_DIR --pyi_out=$DST_DIR $SRC_DIR/metric.proto
#python -m grpc_tools.protoc -I$PROTOS_PATH --python_out=. --pyi_out=. --grpc_python_out=. $PROTOS_PATH/service.proto
