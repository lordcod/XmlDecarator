from tkinter.messagebox import RETRY
from typing import TYPE_CHECKING, Any, Optional
from lxml.etree import ElementBase
from xmlbind.exceptions import DataNotFoundError

if TYPE_CHECKING:
    from xmlbind.root import XmlRoot


class XmlElement:
    def __init__(
        self,
        name: Optional[str] = None,
        *,
        required: bool = False
    ):
        self.name = name
        self.required = required

    def _setup(self, name: str) -> None:
        if self.name is None:
            self.name = name.upper()

    def _parse(self, root: 'XmlRoot', data: ElementBase):
        if not data:
            if self.required:
                raise DataNotFoundError
            return

        return root._parse(data)
