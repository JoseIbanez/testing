"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import logging
import random
import time

import grpc
from service_pb2 import Metric, Ack
from service_pb2_grpc import CollectorStub

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def read_metric() -> dict:
    return {}


def get_metric() -> Metric:

    counter = 0

    while True:

        counter += 1
        metric = parse_metric({})
        yield metric

        if counter > 100000:
            break
        



def parse_metric(raw_metric:dict) -> Metric:

    metric = Metric()
    metric.opco = "VF-UK"
    metric.customer = "Customer 01"
    metric.domain = "Domain 1"
    metric.eventEpoc = int(time.time()*1000)
    metric.resource = "VF0001"
    metric.tags.extend([ 
        Metric.Tag(name="interface", value="G0/1"),
        Metric.Tag(name="hardwaremodel", value="3801G") 
        ])

    metric.values.extend([
        Metric.Value(name="Tx", value=1000.0),
        Metric.Value(name="Rx", value=50.0)
    ])

    return metric

def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = CollectorStub(channel)

        max_time = time.time() + 300
        partial_count = 0
        next_update = 0

        while True:

            raw_metric = read_metric()
            metric = parse_metric(raw_metric)
            stub.SendEvent.future(metric).result()
            partial_count += 1

            if time.time() > max_time:
                break

            if time.time() > next_update:
                next_update = time.time() + 1
                print(f"count {partial_count}")
                partial_count = 0


def run_2():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = CollectorStub(channel)


        result = stub.SendMetricStream(get_metric())
        logger.info("Done. result %s",str(result.code))
        time.sleep(60)



class GrpcAuth(grpc.AuthMetadataPlugin):
    def __init__(self, key):
        self._key = key

    def __call__(self, context, callback):
        callback((('rpc-auth-header', self._key),), None)

def run_3():

    #href: https://grpc.io/docs/guides/auth/


    credentials = grpc.composite_channel_credentials(
        grpc.local_channel_credentials(),
        grpc.metadata_call_credentials(GrpcAuth('token'))
    )

    server = 'localhost:50051'
    server = '192.168.1.22:50051'


    with grpc.secure_channel(server,credentials=credentials) as channel:
        stub = CollectorStub(channel)
        result = stub.SendMetricStream(get_metric())
        logger.info("Done. result %s",str(result.code))
        time.sleep(60)




if __name__ == '__main__':
    logging.basicConfig()
    run_3()