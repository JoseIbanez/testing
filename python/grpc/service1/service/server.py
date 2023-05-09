
from concurrent import futures
import logging
import math
import time
import os

import grpc
from service_pb2 import Point, Feature
import service_pb2_grpc 

from service_pb2 import TenantId, Tenant
from service_pb2 import DeviceId, Device


def get_feature(feature_db, point:Point):
    """Returns Feature at given location or None."""
    for feature in feature_db:

        print(feature)

        if feature.get('v') == point.id:
            return Feature(id=point.id,count=1,message="hi there")

    return None




class RouteGuideServicer(service_pb2_grpc.RouteGuideServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.db = [ {"v":"1"}, {"v":"2"} ]

    def GetFeature(self, request, context):
        feature = get_feature(self.db, request)
        if feature is None:
            return Feature(id="0", count=0, message="")
        else:
            return feature


class InventoryDBServicer(service_pb2_grpc.InventoryDBServicer):



    def __init__(self):

        aviva_tenant = Tenant(id="aviva", name="aviva", sensitivity=0, opco_id="VF-UK", source="aviva-vmanage")
        sandbox_tenant = Tenant(id="sandbox", name="cisco-sandbox", sensitivity=0, opco_id="VGE", source="sandbox-vmanage")

        self.tenant_db = {
            "aviva": aviva_tenant,
            "sandbox": sandbox_tenant
        }


    def GetTenant(self, tenantId:TenantId, context) -> Tenant:

        print(context)

        tenant = self.tenant_db.get(tenantId.id)

        if not tenant:
            return Tenant(id=0,name="",sensitivity=0,opco_id="",source="")

        return tenant




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), 
        server)
    service_pb2_grpc.add_InventoryDBServicer_to_server(
        InventoryDBServicer(),
        server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()