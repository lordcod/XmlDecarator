from enum import Enum
from typing import Generic, Type, TypeVar, Union

T = TypeVar('T')


class XmlCompiler(Generic[T]):
    def __init__(self, validate_type: Union[Type[T], Enum]):
        self.validate_type = validate_type

    def unmarshal(self, v: str) -> T:
        raise NotImplementedError

    def marshal(self, v: T) -> str:
        raise NotImplementedError
