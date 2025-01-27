import itertools
from dataclasses import dataclass, field
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
    parent: 'Node' = field(init=False)
    children: List['Node'] = field(default_factory=list, init=False)

    @property
    def is_multinuclear(self) -> bool:
        return self.relname in ['list', 'same-unit', 'sequence']

    @property
    def siblings(self) -> List[Self]:
        return self.parent.children if self.parent else []

    def get_all_segments(self) -> List['Segment']:
        if isinstance(self, Segment):
            return [self] # TODO não é um caso base
        return list(itertools.chain.from_iterable(child.get_all_segments() for child in self.children))

    # TODO
    def get_text(self) -> str:
        text = ''
        for segment in self.get_all_segments():
            text += segment.get_text()
        return text


@dataclass
class Segment(Node):
    tokens: List[str]
    initial_token_id: int = field(init=False)
    sentence_id: int = field(init=False)

    def get_tokens_ids(self) -> List[int]:
        return list(range(self.initial_token_id, self.initial_token_id + len(self.tokens)))

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
