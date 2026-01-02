#!/bin/bash

set -e

python -m grpc_tools.protoc \
  -I proto \
  --python_out=generated \
  --pyi_out=generated \
  --grpc_python_out=generated \
  proto/findme.proto

# Fixing the import path to be relative
sed -i 's/^import findme_pb2 as/from . import findme_pb2 as/' generated/findme_pb2_grpc.py

echo "Proto files generated successfully"
