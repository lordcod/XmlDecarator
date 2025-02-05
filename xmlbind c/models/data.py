from optparse import Option
from re import L
from typing import Any, Optional
from xmlbind.exceptions import DataNotFoundError


class XmlElementData:
    def __init__(self,
                 name: str,
                 *,
                 required: bool = False):
        self.name = name
        self.required = required

    def _parse(self, data: Any) -> Any:
        if not data and self.required:
            raise DataNotFoundError
        return data
