from dataclasses import dataclass
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

    @classmethod
    def from_element(cls, element: Element) -> Self:
        return cls(
            id=int(element.get('id')),
            parent_id=int(element.get('parent')),
            relname=element.get('relname'),
            type=element.get('type')
        )


@dataclass
class Signal:
    source_id: int
    tokens_ids: List[int]
    type: str
    subtype: str

    @classmethod
    def from_element(cls, element: Element) -> Self:
        return cls(
            source_id=int(element.get('source')),
            tokens_ids=list(map(int, element.get('tokens').split(','))),
            type=element.get('type'),
            subtype=element.get('subtype'),
        )
