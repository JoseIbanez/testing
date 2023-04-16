
export PROTOS_PATH=../protos

python -m grpc_tools.protoc -I$PROTOS_PATH --python_out=. --pyi_out=. --grpc_python_out=. $PROTOS_PATH/service.proto
