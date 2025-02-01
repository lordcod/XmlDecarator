from optparse import Option
from re import L
from typing import Any, Optional
from xmlbind.exceptions import DataNotFoundError
from .adapter import XmlAdapter


class XmlElementData:
    def __init__(self,
                 name: str,
                 *,
                 required: bool = False,
                 adapter: Optional[XmlAdapter] = None):
        self.name = name
        self.required = required
        self.adapter = adapter

    def _parse(self, data: Any) -> Any:
        if self.adapter is not None:
            data = self.adapter(data)
        if not data and self.required:
            raise DataNotFoundError
        return data
