import sys
from . import service_a_pb2

# Register service_a_pb2 in sys.modules so service_a_pb2_grpc can import it
sys.modules['service_a_pb2'] = service_a_pb2

from . import service_a_pb2_grpc

__all__ = ['service_a_pb2', 'service_a_pb2_grpc']
