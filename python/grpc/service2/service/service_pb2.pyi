from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ack(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: int
    def __init__(self, code: _Optional[int] = ...) -> None: ...

class Metric(_message.Message):
    __slots__ = ["customer", "domain", "eventEpoc", "messageVersion", "opco", "resource", "tags", "values"]
    class Tag(_message.Message):
        __slots__ = ["name", "value"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class Value(_message.Message):
        __slots__ = ["name", "value"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: float
        def __init__(self, name: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    EVENTEPOC_FIELD_NUMBER: _ClassVar[int]
    MESSAGEVERSION_FIELD_NUMBER: _ClassVar[int]
    OPCO_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    customer: str
    domain: str
    eventEpoc: int
    messageVersion: int
    opco: str
    resource: str
    tags: _containers.RepeatedCompositeFieldContainer[Metric.Tag]
    values: _containers.RepeatedCompositeFieldContainer[Metric.Value]
    def __init__(self, domain: _Optional[str] = ..., opco: _Optional[str] = ..., customer: _Optional[str] = ..., resource: _Optional[str] = ..., messageVersion: _Optional[int] = ..., eventEpoc: _Optional[int] = ..., values: _Optional[_Iterable[_Union[Metric.Value, _Mapping]]] = ..., tags: _Optional[_Iterable[_Union[Metric.Tag, _Mapping]]] = ...) -> None: ...
