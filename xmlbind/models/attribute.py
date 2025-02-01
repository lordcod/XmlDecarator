from enum import Enum
from typing import Any, List, Optional, Type, Union

from xmlbind.exceptions import DataNotFoundError, ValidateError
from .adapter import XmlAdapter


class XmlAttribute:
    def __init__(
        self,
        name: str,
        *,
        required: bool = False,
        enum: Optional[Union[Enum, Type]] = None,
        adapter: Optional[XmlAdapter] = None
    ):
        self.name = name
        self.required = required
        self.enum = enum
        self.adapter = adapter

    def _parse(self, data: Any):
        if self.adapter:
            data = self.adapter(data)
        if not data and self.required:
            raise DataNotFoundError
        if self.enum is not None:
            try:
                data = self.enum(data)
            except TypeError as exc:
                raise ValidateError from exc

        return data
