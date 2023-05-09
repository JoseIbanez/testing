"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import logging
import random

import grpc
from service_pb2 import Feature, Point
from service_pb2_grpc import RouteGuideStub

from service_pb2_grpc import InventoryDBStub
from service_pb2 import TenantId,Tenant,DeviceId,Device



def guide_get_feature(stub):

    req_point = Point(id="1",count=0, message="p1")

    #feature_future = stub.GetFeature(req_point)
    #feature_future.add_done_callback()

    feature = stub.GetFeature(req_point)
    print(feature, feature.message)




def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = RouteGuideStub(channel)
        stu2 = InventoryDBStub(channel)
        print("-------------- GetFeature --------------")
        guide_get_feature(stub)

        tenantId = TenantId(id="aviva")
        tenant = stu2.GetTenant(tenantId)
        print("tenant:")
        print(tenant)


if __name__ == '__main__':
    logging.basicConfig()
    run()