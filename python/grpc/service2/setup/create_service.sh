
export SRC_DIR=./protos
export DST_DIR=./service

python -m grpc_tools.protoc -I=$SRC_DIR --python_out=$DST_DIR --pyi_out=$DST_DIR --grpc_python_out=$DST_DIR $SRC_DIR/service.proto
