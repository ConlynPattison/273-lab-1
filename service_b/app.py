import json
import time
from flask import Flask, request, jsonify
import grpc
import logging
import os
import sys

# Add parent directory to path to import generated modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import the generated modules and register them in sys.modules
# This is needed because the generated code uses absolute imports
from generated import service_a_pb2, service_a_pb2_grpc

PORT = "8081"
HOST = "localhost"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def check():
    return jsonify(status="ok")

@app.route('/call-echo', methods=['GET'])
def call_echo():
    try:
        start = time.time()
        msg = request.args.get("msg", "")
        with grpc.insecure_channel(f"localhost:8080") as channel:
            stub = service_a_pb2_grpc.ServiceAStub(channel)
            grpc_request = service_a_pb2.EchoRequest(msg=msg)
            grpc_response = stub.Echo(grpc_request, timeout=1.0)
        logging.info(f'service=B endpoint=/call-echo status=ok latency_ms={int((time.time()-start)*1000)}')
        return jsonify(service_b="ok", service_a=json.loads(grpc_response.msg))
    except Exception as error:
        logging.error(f'service=B endpoint=/call-echo status=error error={error}')
        return jsonify(service_b="ok", service_a="unavailable", error=str(error)), 503

app.run(host=HOST, port=PORT, debug=True)
