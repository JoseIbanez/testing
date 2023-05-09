# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import service_pb2 as service__pb2


class RouteGuideStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFeature = channel.unary_unary(
                '/RouteGuide/GetFeature',
                request_serializer=service__pb2.Point.SerializeToString,
                response_deserializer=service__pb2.Feature.FromString,
                )


class RouteGuideServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetFeature(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RouteGuideServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFeature': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFeature,
                    request_deserializer=service__pb2.Point.FromString,
                    response_serializer=service__pb2.Feature.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RouteGuide', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RouteGuide(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetFeature(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RouteGuide/GetFeature',
            service__pb2.Point.SerializeToString,
            service__pb2.Feature.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class InventoryDBStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetTenant = channel.unary_unary(
                '/InventoryDB/GetTenant',
                request_serializer=service__pb2.TenantId.SerializeToString,
                response_deserializer=service__pb2.Tenant.FromString,
                )
        self.GetDevice = channel.unary_unary(
                '/InventoryDB/GetDevice',
                request_serializer=service__pb2.DeviceId.SerializeToString,
                response_deserializer=service__pb2.Device.FromString,
                )
        self.SaveTenant = channel.unary_unary(
                '/InventoryDB/SaveTenant',
                request_serializer=service__pb2.Tenant.SerializeToString,
                response_deserializer=service__pb2.Tenant.FromString,
                )
        self.SaveDevice = channel.unary_unary(
                '/InventoryDB/SaveDevice',
                request_serializer=service__pb2.Device.SerializeToString,
                response_deserializer=service__pb2.Device.FromString,
                )


class InventoryDBServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetTenant(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDevice(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveTenant(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveDevice(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_InventoryDBServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetTenant': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTenant,
                    request_deserializer=service__pb2.TenantId.FromString,
                    response_serializer=service__pb2.Tenant.SerializeToString,
            ),
            'GetDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDevice,
                    request_deserializer=service__pb2.DeviceId.FromString,
                    response_serializer=service__pb2.Device.SerializeToString,
            ),
            'SaveTenant': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveTenant,
                    request_deserializer=service__pb2.Tenant.FromString,
                    response_serializer=service__pb2.Tenant.SerializeToString,
            ),
            'SaveDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveDevice,
                    request_deserializer=service__pb2.Device.FromString,
                    response_serializer=service__pb2.Device.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'InventoryDB', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class InventoryDB(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetTenant(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/InventoryDB/GetTenant',
            service__pb2.TenantId.SerializeToString,
            service__pb2.Tenant.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/InventoryDB/GetDevice',
            service__pb2.DeviceId.SerializeToString,
            service__pb2.Device.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveTenant(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/InventoryDB/SaveTenant',
            service__pb2.Tenant.SerializeToString,
            service__pb2.Tenant.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/InventoryDB/SaveDevice',
            service__pb2.Device.SerializeToString,
            service__pb2.Device.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
