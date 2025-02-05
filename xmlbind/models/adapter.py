from typing import Generic, TypeVar

K = TypeVar('K')
V = TypeVar('V')


class XmlAdapter(Generic[K, V]):
    def __init__(self):
        super().__init__()

    def _parse(self, data: K) -> V:
        return data

    def __call__(self, data: K) -> V:
        if not data:
            return None
        return self._parse(data)
