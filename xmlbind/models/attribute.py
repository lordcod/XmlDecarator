from enum import Enum
from typing import Any, List, Optional, Type, Union

from xmlbind.compiler import XmlCompiler
from xmlbind.exceptions import DataNotFoundError, ValidateError
from xmlbind.settings import get_compiler


class XmlAttribute:
    def __init__(
        self,
        name: Optional[str] = None,
        *,
        required: bool = False,
        enum: Optional[Union[Enum, Type]] = None,
        adapter: Optional[XmlCompiler] = None
    ):
        self.name = name
        self.required = required
        self.enum = enum
        self.adapter = adapter

    def _setup(self,  name: str) -> None:
        if self.name is None:
            self.name = name

    def _parse(self, _type: Type, data: Any):
        if self.adapter:
            data = self.adapter.unmarshal(data)
        elif compiler := get_compiler(_type):
            data = compiler.unmarshal(data)
        elif issubclass(_type, Enum):
            self.enum = _type

        if data is None:
            if self.required:
                raise DataNotFoundError
            return

        if self.enum is not None:
            try:
                data = self.enum(data)
            except TypeError as exc:
                raise ValidateError from exc

        return data
