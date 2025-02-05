from typing import TYPE_CHECKING, Any, Optional
from xmlbind.exceptions import DataNotFoundError
from .element import XmlElement
from lxml.etree import ElementBase

if TYPE_CHECKING:
    from xmlbind.root import XmlRoot


class XmlElementWrapper:
    def __init__(
        self,
        name: Optional[str] = None,
        element_name: Optional[str] = None,
        *,
        required: bool = False,
        with_list: Optional[bool] = None
    ):
        self.name = name
        self.element_name = element_name
        self.required = required
        self.with_list = with_list

    def _setup(self, name: str, element_name: str, with_list: bool) -> None:
        if self.name is None:
            self.name = name.upper()
        if self.element_name is None:
            self.element_name = element_name.upper()
        if self.with_list is None:
            self.with_list = with_list

    def _parse(self, root: 'XmlRoot', data: ElementBase):
        if not (data is not None and len(data) > 0 and data.findall(self.element_name)):
            if self.required:
                raise DataNotFoundError(self.name, self.element_name)
            return

        elements = data.findall(self.element_name)
        ret = [root._parse(el) for el in elements]
        if self.with_list:
            return ret
        elif len(ret) > 0:
            return ret[0]
