# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: logger.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'logger.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0clogger.proto\x12\x06logger\"$\n\x11LogMessageRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x17\n\x15GetListMessageRequest\"!\n\x0fLogMessageReply\x12\x0e\n\x06result\x18\x01 \x01(\t\"(\n\x14ListLogMessagesReply\x12\x10\n\x08messages\x18\x01 \x03(\t2\x9e\x01\n\x06Logger\x12\x43\n\x0bSaveMessage\x12\x19.logger.LogMessageRequest\x1a\x17.logger.LogMessageReply\"\x00\x12O\n\x0eGetAllMessages\x12\x1d.logger.GetListMessageRequest\x1a\x1c.logger.ListLogMessagesReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'logger_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_LOGMESSAGEREQUEST']._serialized_start=24
  _globals['_LOGMESSAGEREQUEST']._serialized_end=60
  _globals['_GETLISTMESSAGEREQUEST']._serialized_start=62
  _globals['_GETLISTMESSAGEREQUEST']._serialized_end=85
  _globals['_LOGMESSAGEREPLY']._serialized_start=87
  _globals['_LOGMESSAGEREPLY']._serialized_end=120
  _globals['_LISTLOGMESSAGESREPLY']._serialized_start=122
  _globals['_LISTLOGMESSAGESREPLY']._serialized_end=162
  _globals['_LOGGER']._serialized_start=165
  _globals['_LOGGER']._serialized_end=323
# @@protoc_insertion_point(module_scope)