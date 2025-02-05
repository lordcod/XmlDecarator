from typing import Any, Optional, get_args, get_origin
from lxml.etree import ElementBase, Element
from xmlbind.models import (XmlAttribute, XmlElementData,
                            XmlElement, XmlElementWrapper)
from xmlbind.settings import get_compiler
from xmlbind.exceptions import DataNotFoundError
xml_objects = (XmlAttribute, XmlElementData,
               XmlElement, XmlElementWrapper)


class ParseError(Exception):
    pass


def get_valid_annot(annot: Any):
    return annot


def _parse_annot(annot: Any):
    annot = get_valid_annot(annot)
    if type(annot) is type and issubclass(annot, XmlRoot):
        return annot
    elif get_origin(annot) is not None:
        return get_args(annot)[0]
    raise TypeError('Not found annot')


def _is_annot_list(annot: Any):
    annot = get_valid_annot(annot)
    if type(annot) is type and issubclass(annot, XmlRoot):
        return False
    elif get_origin(annot) is not None:
        return True
    raise TypeError('Not found annot')


class XmlRoot:
    def __init__(self, **kwargs) -> None:
        cls = type(self)

        for k, v in kwargs.items():
            if v is None:
                continue

            if not isinstance(getattr(cls, k),
                              (XmlAttribute, XmlElementWrapper, XmlElement)):
                raise TypeError(
                    'It is impossible to assign a key value to %s' % k)

            setattr(self, k, v)

        self._ofter_init()

    def __init_subclass__(cls):
        annotations = cls.__annotations__
        for name, value in cls.__dict__.items():
            if isinstance(value, XmlElement):
                value._setup(name)
            if isinstance(value, XmlElementWrapper):
                annot = annotations[name]
                annot = get_valid_annot(annot)
                value._setup(name, annot.__name__, _is_annot_list(annot))
            if isinstance(value, XmlAttribute):
                value._setup(name)

    def _ofter_init(self) -> None:
        for name, value in self.__class__.__dict__.items():
            if not isinstance(value, (XmlElement, XmlAttribute, XmlElementWrapper)):
                continue
            if name in self.__dict__:
                continue
            if value.required:
                raise DataNotFoundError(name)
            if isinstance(value, XmlElementWrapper) and value.with_list:
                setattr(self, name, [])
            else:
                setattr(self, name, None)

    @classmethod
    def _parse(cls, element: ElementBase):
        self = cls.__new__(cls)
        annotations = cls.__annotations__
        for name, value in cls.__dict__.items():
            try:
                if isinstance(value, (XmlElement, XmlElementWrapper)):
                    setattr(self, name, value._parse(_parse_annot(annotations[name]),
                                                     element.find(value.name)))
                if isinstance(value, XmlAttribute):
                    annot = get_valid_annot(annotations[name])
                    setattr(self, name, value._parse(annot, element.get(value.name)))
                if isinstance(value, XmlElementData):
                    setattr(self, name, value._parse(element.find(value.name)))
            except Exception as exc:
                raise ParseError('Processing error on the %s %s element, tag root: %s' % (value.name, type(value).__name__, element.tag)) from exc
        return self

    def dump(self, tag: Optional[str] = None, /) -> ElementBase:
        data = self.__dict__
        cls_data = type(self).__dict__
        attrib = {}
        children = []

        for name, value in data.items():
            if not isinstance(value, (XmlRoot, list)):
                continue
            if isinstance(value, list) and (len(value) == 0 or not isinstance(value[0], XmlRoot)):
                continue

            xml_element = cls_data[name]
            if isinstance(xml_element, XmlElement):
                element = value.dump(xml_element.name)
            elif isinstance(xml_element, XmlElementWrapper):
                if isinstance(value, XmlRoot):
                    elements = [value.dump(xml_element.element_name)]
                else:
                    elements = [v.dump(xml_element.element_name) for v in value]
                element = Element(xml_element.name)
                element.extend(elements)
            else:
                raise ValueError('The data type for class %s was not found.' % name)
            children.append(element)

        for name, value in cls_data.items():
            if not isinstance(value, XmlAttribute):
                continue

            try:
                atr = data[name]
            except KeyError as ke:
                if value.required:
                    raise
                else:
                    print(ke, name, data)
                    continue

            if value.adapter:
                data = value.adapter.unmarshal(data)
            elif compiler := get_compiler(type(atr)):
                atr = compiler.marshal(atr)

            if not atr:
                continue
            attrib[value.name] = atr

        el = Element(
            tag,
            attrib=attrib
        )
        el.extend(children)
        return el

    def __repr__(self):
        kwargs = {k: v for k, v in self.__dict__.items()
                  if not k.startswith('_')}
        return '<%s %s>' % (type(self).__name__,
                            ' '.join(f'{k}={v}'
                                     for k, v in kwargs.items()))
