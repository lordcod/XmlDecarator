from typing import TYPE_CHECKING, Any, Optional
from xmlbind.exceptions import DataNotFoundError
from .adapter import XmlAdapter
from .element import XmlElement
from lxml.etree import ElementBase

if TYPE_CHECKING:
    from xmlbind.root import XmlRoot


class XmlElementWrapper:
    def __init__(
        self,
        name: str,
        element_name: str,
        *,
        required: bool = False,
        with_list: Optional[bool] = None,
        adapter: Optional[XmlAdapter[ElementBase, ElementBase]] = None
    ):
        self.name = name
        self.element_name = element_name
        self.required = required
        self.with_list = with_list
        self.adapter = adapter

    def _parse(self, root: 'XmlRoot', data: ElementBase):
        if self.adapter:
            data = self.adapter(data)
        if self.required and (
            not data
            or not data.findall(self.element_name)
        ):
            raise DataNotFoundError
        elements = data.findall(self.element_name)
        ret = [root._parse(el) for el in elements]
        return ret if self.with_list else len(ret) > 0 and ret[0]
