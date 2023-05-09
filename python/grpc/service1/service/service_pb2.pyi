from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Device(_message.Message):
    __slots__ = ["id", "management_ip", "model", "name", "tenant_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MANAGEMENT_IP_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    management_ip: str
    model: str
    name: str
    tenant_id: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., tenant_id: _Optional[str] = ..., management_ip: _Optional[str] = ..., model: _Optional[str] = ...) -> None: ...

class DeviceId(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class Feature(_message.Message):
    __slots__ = ["count", "id", "message"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    count: int
    id: str
    message: str
    def __init__(self, id: _Optional[str] = ..., count: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class Point(_message.Message):
    __slots__ = ["count", "id", "message"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    count: int
    id: str
    message: str
    def __init__(self, id: _Optional[str] = ..., count: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class Tenant(_message.Message):
    __slots__ = ["id", "name", "opco_id", "sensitivity", "source"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPCO_ID_FIELD_NUMBER: _ClassVar[int]
    SENSITIVITY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    opco_id: str
    sensitivity: int
    source: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., sensitivity: _Optional[int] = ..., opco_id: _Optional[str] = ..., source: _Optional[str] = ...) -> None: ...

class TenantId(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...
