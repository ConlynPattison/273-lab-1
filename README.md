# Lab 1

Goal: Build a tiny, locally distributed system with two services that communicate over the network, include basic logging, and demonstrate independent failure.

---

## Services

### service_a

- Provider
- gRPC server using python+grpc
- Can handle basic requests
- `localhost:8080`

Start locally:

```bsh
cd service_a
python -m venv .venv_a
source .venv_a/bin/activate
pip install -r requirements.txt
python app.py
```

### service_b

- Consumer
- HTTP server using python+flask
- Behaves correctly when A is not available or slow
- `GET /health → {"status":"ok"}`
- `GET /call-echo?msg=hello`
- `localhost:8081`

Start locally:

```bsh
cd service_b
python -m venv .venv_b
source .venv_b/bin/activate
pip install -r requirements.txt
python app.py
```

### proto generation

Generating protocols and types files:

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

---

## Q&A

### How to run locally?

Local terminal commands are provided above for starting service A, starting service B, and gRPC protocol buffer generation.

To request the call-echo endpoint from service B, run the following within a new terminal:

```bsh
curl "http://localhost:8081/call-echo?msg=test"
```

### Proof of success and failure

**Note: Each of these cases assume that the virtual environments are started, dependencies are installed, and protocol buffer files are generated**

#### Successful case

1. Begin both service processes in separate terminals.

image

2. Make request call to service B from a separate terminal process and view successful combined response and logging.

image

#### Failure case - service unavilable

1. Begin only service B.

image

2. Make request call to service B from a separate terminal process and view failure to connect, combined response, and logging.

image

#### Failure case - service slow

1. Begin service B and service A, but use delay flag and value in launching service A.

image

2. Make request call to service B from a separate terminal process and view timeout failure, combined response, and logging.

image

### What makes this distributed?

This is a distributed system because we have two separate processes running and communicating across a network. Each service is able to both operate and fail independently without cascading fail stops across components.
