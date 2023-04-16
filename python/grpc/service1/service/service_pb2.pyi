from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

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
