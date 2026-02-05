import argparse
from concurrent import futures
import time
import grpc
import json
import logging
import sys
import os

# Add parent directory to path to import generated modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import the generated modules and register them in sys.modules
# This is needed because the generated code uses absolute imports
from generated import service_a_pb2, service_a_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--delay", help="force delay in response time by second(s)", type=int, action="store", default=0)
args = parser.parse_args()

DELAY = min(max(args.delay, 0), 5)
SERVICE_NAME = "service_a"
SERVICE_HOST = "localhost"
SERVICE_PORT = "8080"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ServiceProvider():
    def Echo(
            self, 
            request: service_a_pb2.EchoRequest, 
            context: grpc.ServicerContext
    ) -> service_a_pb2.EchoReply:
        start = time.time()

        # Simulate a delay
        time.sleep(DELAY)

        logging.info(f'service=A procedure=Echo status=ok latency_ms={int((time.time()-start)*1000)}')
        return service_a_pb2.EchoReply(msg=json.dumps({"echo": request.msg}))
    
    def HealthCheck(
            self,
            request: service_a_pb2.HealthCheckRequest,
            context: grpc.ServicerContext
    ) -> service_a_pb2.HealthCheckReply:
        return service_a_pb2.HealthCheckReply(status="ok")
    
def serve(host: str = SERVICE_HOST, port: int = SERVICE_PORT) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    service_a_pb2_grpc.add_ServiceAServicer_to_server(ServiceProvider(), server)

    server.add_insecure_port(f"{host}:{port}")
    server.start()
    print(f"gRPC server listening on {host}:{port}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
