from dataclasses import dataclass, KW_ONLY, field
from typing import List, Self
from xml.etree.ElementTree import Element


@dataclass
class Relation:
    name: str
    type: str

    @classmethod
    def from_element(cls, element: Element) -> Self:
        return cls(element.get('name'), element.get('type'))


@dataclass
class Node:
    id: int
    parent_id: int
    relname: str
    signals: List['Signal'] = field(default_factory=list, init=False)
    parent: Self = field(init=False)

    @property
    def is_multinuclear(self) -> bool:
        return self.relname in ['list', 'same-unit']


@dataclass
class Segment(Node):
    tokens: List[str]

    @classmethod
    def from_element(cls, element: Element) -> Self:
        return cls(
            id=int(element.get('id')),
            parent_id=int(element.get('parent')),
            relname=element.get('relname'),
            tokens=element.text.split()
        )


@dataclass
class Group(Node):
    type: str
    parent_id: int | None

    @classmethod
    def from_element(cls, element: Element) -> Self:
        parent = element.get('parent')
        return cls(
            id=int(element.get('id')),
            parent_id=int(parent) if parent else None,
            relname=element.get('relname'),
            type=element.get('type')
        )


@dataclass
class Signal:
    id: int
    source_id: int
    tokens_ids: List[int]
    type: str
    subtype: str
    source: Node = None

    @classmethod
    def from_element(cls, element: Element, signal_id: int) -> Self:
        return cls(
            id=signal_id,
            source_id=int(element.get('source')),
            tokens_ids=list(map(int, element.get('tokens').split(','))),
            type=element.get('type'),
            subtype=element.get('subtype'),
        )
