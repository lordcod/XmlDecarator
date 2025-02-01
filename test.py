from datetime import datetime
import lxml.etree as ET
from xmlbind.compiler import XmlCompiler
from xmlbind.root import XmlRoot
from xmlbind.models import XmlAttribute
from xmlbind.models.wrapper import XmlElementWrapper
from xmlbind.settings import add_compiler


class Meet(XmlRoot):
    name: str = XmlAttribute()
    city: str = XmlAttribute()
    date: datetime = XmlAttribute()


class Lenex(XmlRoot):
    version: str = XmlAttribute()
    meet: Meet = XmlElementWrapper('MEETS', 'MEET')


class DtCompiler(XmlCompiler[datetime]):
    def __init__(self):
        super().__init__(datetime)

    def unmarshal(self, v):
        return datetime.strptime(v, "%Y-%m-%d")


if __name__ == '__main__':
    add_compiler(DtCompiler())

    element = ET.fromstring(
        open('test.xml', 'rb').read())
    lenex = Lenex._parse(element)

    print(lenex, lenex.version, lenex.meet)
