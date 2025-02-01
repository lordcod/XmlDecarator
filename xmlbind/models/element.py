from tkinter.messagebox import RETRY
from typing import TYPE_CHECKING, Any, Optional
from lxml.etree import ElementBase
from xmlbind.exceptions import DataNotFoundError
from .adapter import XmlAdapter

if TYPE_CHECKING:
    from xmlbind.root import XmlRoot


class XmlElement:
    def __init__(
        self,
        name: str,
        *,
        required: bool = False,
        adapter: Optional[XmlAdapter[ElementBase, ElementBase]] = None
    ):
        self.name = name
        self.adapter = adapter
        self.required = required

    def _parse(self, root: 'XmlRoot', data: ElementBase):
        if self.adapter:
            data = self.adapter(data)
        if not data and self.required:
            raise DataNotFoundError
        return root._parse(data)
