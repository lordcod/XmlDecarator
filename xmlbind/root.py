from typing import Any, get_args, get_origin
import lxml.etree as ET
from lxml.etree import Element, ElementBase
from xmlbind.models import (XmlAttribute, XmlElementData,
                            XmlElement, XmlElementWrapper)
xml_objects = (XmlAttribute, XmlElementData,
               XmlElement, XmlElementWrapper)


def _parse_annot(annot: Any):
    if issubclass(annot, XmlRoot):
        return annot
    elif get_origin(annot) is not None:
        return get_args(annot)[0]
    raise TypeError('Not found annot')


class XmlRoot:
    @classmethod
    def _parse(cls, element: ElementBase):
        self = cls()
        annotations = cls.__annotations__
        for name, value in cls.__dict__.items():
            if isinstance(value, (XmlElement, XmlElementWrapper)):
                setattr(self, name, value._parse(_parse_annot(annotations[name]),
                                                 element.find(value.name)))
            if isinstance(value, XmlAttribute):
                setattr(self, name, value._parse(element.get(value.name)))
            if isinstance(value, XmlElementData):
                setattr(self, name, value._parse(element.find(value.name)))
        return self
