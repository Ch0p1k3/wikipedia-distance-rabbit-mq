# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\"9\n\x0f\x44istanceRequest\x12\x12\n\nsource_url\x18\x01 \x01(\t\x12\x12\n\ntarget_url\x18\x02 \x01(\t\"\x1d\n\rDistanceReply\x12\x0c\n\x04path\x18\x01 \x03(\t2C\n\x11WikipediaDistance\x12.\n\x08\x44istance\x12\x10.DistanceRequest\x1a\x0e.DistanceReply\"\x00\x62\x06proto3')



_DISTANCEREQUEST = DESCRIPTOR.message_types_by_name['DistanceRequest']
_DISTANCEREPLY = DESCRIPTOR.message_types_by_name['DistanceReply']
DistanceRequest = _reflection.GeneratedProtocolMessageType('DistanceRequest', (_message.Message,), {
  'DESCRIPTOR' : _DISTANCEREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:DistanceRequest)
  })
_sym_db.RegisterMessage(DistanceRequest)

DistanceReply = _reflection.GeneratedProtocolMessageType('DistanceReply', (_message.Message,), {
  'DESCRIPTOR' : _DISTANCEREPLY,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:DistanceReply)
  })
_sym_db.RegisterMessage(DistanceReply)

_WIKIPEDIADISTANCE = DESCRIPTOR.services_by_name['WikipediaDistance']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DISTANCEREQUEST._serialized_start=17
  _DISTANCEREQUEST._serialized_end=74
  _DISTANCEREPLY._serialized_start=76
  _DISTANCEREPLY._serialized_end=105
  _WIKIPEDIADISTANCE._serialized_start=107
  _WIKIPEDIADISTANCE._serialized_end=174
# @@protoc_insertion_point(module_scope)
