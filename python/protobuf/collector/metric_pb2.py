# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: metric.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cmetric.proto\x12\tprotoblog\"\x8d\x02\n\x06Metric\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12\x0c\n\x04opco\x18\x02 \x01(\t\x12\x10\n\x08\x63ustomer\x18\x03 \x01(\t\x12\x10\n\x08resource\x18\x04 \x01(\t\x12\x16\n\x0emessageVersion\x18\x05 \x01(\r\x12\x11\n\teventEpoc\x18\x06 \x01(\r\x12\'\n\x06values\x18\x07 \x03(\x0b\x32\x17.protoblog.Metric.Value\x12#\n\x04tags\x18\x08 \x03(\x0b\x32\x15.protoblog.Metric.Tag\x1a$\n\x05Value\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02\x1a\"\n\x03Tag\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'metric_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _METRIC._serialized_start=28
  _METRIC._serialized_end=297
  _METRIC_VALUE._serialized_start=225
  _METRIC_VALUE._serialized_end=261
  _METRIC_TAG._serialized_start=263
  _METRIC_TAG._serialized_end=297
# @@protoc_insertion_point(module_scope)
