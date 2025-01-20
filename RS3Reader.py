import os

from typing import List, Dict
from xml.etree import ElementTree

from elements import Relation, Group, Segment, Signal, Node


class RS3Reader:
    def __init__(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Document at "{file_path}" does not exist')

        self.tree = ElementTree.parse(file_path)
        self.root = self.tree.getroot()
        self.relations = self.get_relations()
        self.groups = self.get_groups()
        self.segments = self.get_segments()
        self.signals = self.get_signals()
        self._link_nodes()

    def _link_nodes(self):
        for node in self.nodes.values():
            node.parent = self.nodes.get(node.parent_id)
        for signal in self.signals.values():
            signal.source = self.nodes.get(signal.source_id)
            signal.source.signals.append(signal)

    @property
    def nodes(self) -> Dict[int, Node]:
        nodes = self.segments | self.groups
        return nodes

    def get_relations(self) -> List[Relation]:
        relations_elements = self.root.findall('header/relations/rel')
        relations = list(map(Relation.from_element, relations_elements))
        return relations

    def get_groups(self) -> Dict[int, Group]:
        groups_elements = self.root.findall('body/group')
        groups = {group.id: group for group in map(Group.from_element, groups_elements)}
        return groups

    def get_segments(self) -> Dict[int, Segment]:
        segments_elements = self.root.findall('body/segment')
        segments = {segment.id: segment for segment in map(Segment.from_element, segments_elements)}
        return segments

    def get_signals(self) -> Dict[int, Signal]:
        signals_elements = self.root.findall('body/signals/signal')
        signals = {i: Signal.from_element(signals_elements[i], i) for i in range(len(signals_elements))}
        return signals
