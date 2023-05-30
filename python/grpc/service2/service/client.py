"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import logging
import random
import time
import os

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

        if counter > 1000:
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

    server = 'localhost:50051'
    server = 'h3.loc:50051'

    with grpc.insecure_channel(server) as channel:
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

    server =  os.environ.get('GRPC_TARGET','localhost:50051')


    if "443" in server:

        # build ssl credentials using the cert the same as before
        with open('./setup/roots.pem', 'rb') as f:
            cert = f.read()

        channel_security="ssl"
        credentials = grpc.composite_channel_credentials(
            grpc.ssl_channel_credentials(cert),
            grpc.metadata_call_credentials(GrpcAuth('token'))
        )
        channel = grpc.secure_channel(server,credentials=credentials)

    elif "127.0.0.1" in server:
        channel_security = "local"
        credentials = grpc.composite_channel_credentials(
            grpc.local_channel_credentials(),
            grpc.metadata_call_credentials(GrpcAuth('token'))
        )
        channel = grpc.secure_channel(server,credentials=credentials)

    else:
        channel_security = "insecure"
        channel = grpc.insecure_channel(server)


    logger.info("Connecting gRPC target:%s, channel:%s",server,channel_security)

    #gen_metric = get_metric()
    #metric_list = iter( [next(gen_metric), next(gen_metric)])



    with channel:
        stub = CollectorStub(channel)
        result = stub.SendMetricStream(get_metric()) # metric_list ) #get_metric())
        logger.info("Done. resultCode:%s",str(result.code))




if __name__ == '__main__':
    logging.basicConfig()

    for round in range(1,200):
        run_3()