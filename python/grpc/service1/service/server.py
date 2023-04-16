
from concurrent import futures
import logging
import math
import time
import os

import grpc
from service_pb2 import Point, Feature
import service_pb2_grpc 


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



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), 
        server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()