import lxml.etree as ET
from xmlbind.root import XmlRoot
from xmlbind.models import XmlAttribute
from xmlbind.models.wrapper import XmlElementWrapper


class Meet(XmlRoot):
    name: str = XmlAttribute('name')
    city: str = XmlAttribute('city')


class Lenex(XmlRoot):
    version: str = XmlAttribute('version')
    meet: Meet = XmlElementWrapper('MEETS', 'MEET', with_list=False)


if __name__ == '__main__':
    element = ET.fromstring(
        open('test.xml', 'rb').read())
    lenex = Lenex._parse(element)

    print(lenex, lenex.version, lenex.meet.name, lenex.meet.city)
