# Lab 1

## Services

**service_a**

- Provider
- gRPC server
- Can handle basic requests
- `localhost:8080`

**service_b**

- Consumer
- HTTP server using Python Flask
- Behaves correctly when A is not available or slow
- `localhost:8081`

## gRPC proto

```bsh
cd proto_build
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m grpc_tools.protoc \
  -I ../protos \
  --python_out=../generated \
  --grpc_python_out=../generated \
  --mypy_out=../generated \
  ../protos/service_a.proto
```
