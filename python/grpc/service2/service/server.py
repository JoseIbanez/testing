
from concurrent import futures
import logging
import math
import time
import os

import grpc
from service_pb2 import Metric, Ack
import service_pb2_grpc 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ESM_Kafka:

    def __init__(self):
        self.partial_counter = 0
        self.next_update = 0

    def send(self, metric:Metric):

        #print(metric)
        self.partial_counter += 1

        if time.time() > self.next_update:
            logger.info("Server %d",self.partial_counter)
            self.partial_counter = 0
            self.next_update = time.time()+1


        return


class CollectorServicer(service_pb2_grpc.CollectorServicer):
    """
    Provides methods that implement functionality of collector server.
    """
    def __init__(self) -> None:
        self.kafka = ESM_Kafka()
        super().__init__()

    

    def SendEvent(self, request, context) -> Ack:
        self.kafka.send(request)
        return Ack(code=0)


    def SendMetricStream(self, request_iterator, context) -> Ack:

        logger.info("invocation_metadata: %s",context.invocation_metadata())
        count = 0
        time0 = time.time()

        for request in request_iterator:
            count += 1
            self.kafka.send(request)

        logger.info("Items %d, delay %.03f. Done",count,time.time()-time0)

        return Ack(code=0)


class AuthInterceptor(grpc.ServerInterceptor):
    def __init__(self, key):
        self._valid_metadata = ('rpc-auth-header', key)

        def deny(_, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid key')

        self._deny = grpc.unary_unary_rpc_method_handler(deny)

    def intercept_service(self, continuation, handler_call_details):
        meta = handler_call_details.invocation_metadata

        #print(meta)

        if 1 or meta and meta[0] == self._valid_metadata:
            return continuation(handler_call_details)
        else:
            return self._deny


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(AuthInterceptor('token'),))

    service_pb2_grpc.add_CollectorServicer_to_server(
        CollectorServicer(),
        server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()