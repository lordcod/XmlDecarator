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


def _is_annot_list(annot: Any):
    if issubclass(annot, XmlRoot):
        return False
    elif get_origin(annot) is not None:
        return True
    raise TypeError('Not found annot')


class XmlRoot:
    def __init_subclass__(cls):
        annotations = cls.__annotations__
        for name, value in cls.__dict__.items():
            if isinstance(value, XmlElement):
                value._setup(name)
            if isinstance(value, XmlElementWrapper):
                annot = annotations[name]
                value._setup(name, annot.__name__, _is_annot_list(annot))
            if isinstance(value, XmlAttribute):
                value._setup(name)

    @classmethod
    def _parse(cls, element: ElementBase):
        self = cls()
        annotations = cls.__annotations__
        for name, value in cls.__dict__.items():
            if isinstance(value, (XmlElement, XmlElementWrapper)):
                setattr(self, name, value._parse(_parse_annot(annotations[name]),
                                                 element.find(value.name)))
            if isinstance(value, XmlAttribute):
                setattr(self, name, value._parse(annotations[name], element.get(value.name)))
            if isinstance(value, XmlElementData):
                setattr(self, name, value._parse(element.find(value.name)))
        return self

    def __repr__(self):
        kwargs = {k: v for k, v in self.__dict__.items()
                  if not k.startswith('_')}
        return '<%s %s>' % (type(self).__name__,
                            ' '.join(f'{k}={v}'
                                     for k, v in kwargs.items()))
