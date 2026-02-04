# Lab 1

## Services

### service_a

Description:

- Provider
- gRPC server using python+grpc
- Can handle basic requests
- `localhost:8080`

Run locally:

```bsh
cd service_a
python -m venv .venv_a
source .venv_a/bin/activate
pip install -r requirements.txt
python app.py
```

### service_b

Description:

- Consumer
- HTTP server using python+flask
- Behaves correctly when A is not available or slow
- `GET /health → {"status":"ok"}`
- `GET /call-echo?msg=hello`
- `localhost:8081`

Generating protocols and types:

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

Run locally:

```bsh
cd service_b
python -m venv .venv_b
source .venv_b/bin/activate
pip install -r requirements.txt
python app.py
```

---

## Q&A

### How to run locally?

Local terminal commands provided above for Service A, Service B, and gRPC protocol buffer generation.

### Proof of success and failure?

### What makes this distributed?
