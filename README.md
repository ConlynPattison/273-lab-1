# Lab 1

Goal: Build a tiny, locally distributed system with two services that communicate over the network, include basic logging, and demonstrate independent failure.

---

## Services

### service_a

- Provider
- gRPC server using Python+grpc
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
- HTTP server using Python+Flask
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

## Other Deliverables

### How to run locally?

Local terminal commands are provided above for starting service A, starting service B, and generating gRPC protocol buffers.

To request the call-echo endpoint from service B, run the following within a new terminal:

```bsh
curl "http://localhost:8081/call-echo?msg=test"
```

### Proof of success and failure

**Note: Each of these cases assume that the virtual environments are started, dependencies are installed, and protocol buffer files are generated**

#### Successful case

1. Begin both service processes in separate terminals.

<img width="1369" height="241" alt="image" src="https://github.com/user-attachments/assets/9e15ec27-44e4-4fdc-8d31-deb4c13d5b73" />

2. Make request call to service B from a separate terminal process and view successful combined response and logging.

<img width="766" height="311" alt="image" src="https://github.com/user-attachments/assets/919cdd08-a0ef-49a5-b2c6-da8085697f89" />

<img width="1351" height="412" alt="image" src="https://github.com/user-attachments/assets/1aa09bcb-cd01-4a4e-b883-398a377c8a46" />

#### Failure case - service unavilable

1. Begin only service B.

<img width="1351" height="411" alt="image" src="https://github.com/user-attachments/assets/f0c5ab5c-3917-4350-949f-c8ff522d3d2b" />

2. Make request call to service B from a separate terminal process and view failure to connect, 503 code, combined response, and logging.

<img width="1351" height="412" alt="image" src="https://github.com/user-attachments/assets/c98c12fd-24da-4cc1-8103-6ba4ac00d8ba" />

<img width="763" height="310" alt="image" src="https://github.com/user-attachments/assets/508bd1b0-1e47-4ccd-9cbc-4421e6c9660b" />

#### Failure case - service slow

1. Begin service B and service A, but use delay flag and value in launching service A.

<img width="1353" height="410" alt="image" src="https://github.com/user-attachments/assets/d6d95fe6-cc8c-4016-adb9-c8b2beffc825" />

2. Make request call to service B from a separate terminal process and view timeout failure, combined response, and logging.

<img width="1351" height="409" alt="image" src="https://github.com/user-attachments/assets/5fbfa52d-fde7-41eb-9aec-04edfdbc524d" />

<img width="766" height="313" alt="image" src="https://github.com/user-attachments/assets/bc975cb6-f31b-4055-b490-531811a1df14" />

### What makes this distributed?

This is a distributed system because we have two separate processes running and communicating across a network.
Each service can fail independently without cascading across components.
Being separate Python processes, they also do not share the same memory space and could be deployed to not share the same clock.
