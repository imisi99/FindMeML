#!/bin/bash

set -e

python -m grpc_tools.protoc \
  -I proto \
  --python_out=generated \
  --pyi_out=generated \
  --grpc_python_out=generated \
  proto/emb.proto

# Fixing the import path to be relative
sed -i 's/^import emb_pb2 as/from . import emb_pb2 as/' generated/emb_pb2_grpc.py

echo "Proto files generated successfully"
