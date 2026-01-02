from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserEmbeddingRequest(_message.Message):
    __slots__ = ("user_id", "bio", "skills", "interests")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    SKILLS_FIELD_NUMBER: _ClassVar[int]
    INTERESTS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    bio: str
    skills: _containers.RepeatedScalarFieldContainer[str]
    interests: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, user_id: _Optional[str] = ..., bio: _Optional[str] = ..., skills: _Optional[_Iterable[str]] = ..., interests: _Optional[_Iterable[str]] = ...) -> None: ...

class ProjectEmbeddingRequest(_message.Message):
    __slots__ = ("project_id", "title", "description", "skills")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SKILLS_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    title: str
    description: str
    skills: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, project_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., skills: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteEmbeddingRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class EmbeddingResponse(_message.Message):
    __slots__ = ("success", "msg")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    success: bool
    msg: str
    def __init__(self, success: bool = ..., msg: _Optional[str] = ...) -> None: ...
