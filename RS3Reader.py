import os
from typing import List
from xml.etree import ElementTree

from elements import Relation, Group, Segment, Signal


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

    def get_relations(self) -> List[Relation]:
        relations_elements = self.root.findall('header/relations/rel')
        relations = [Relation.from_element(element) for element in relations_elements]
        return relations

    def get_groups(self) -> List[Group]:
        group_elements = self.root.findall('body/group')
        groups = [Group.from_element(element) for element in group_elements]
        return groups

    def get_segments(self) -> List[Segment]:
        segments_elements = self.root.findall('body/segment')
        segments = [Segment.from_element(element) for element in segments_elements]
        return segments

    def get_signals(self) -> List[Signal]:
        signals_elements = self.root.findall('body/signals/signal')
        signals = [Signal.from_element(element) for element in signals_elements]
        return signals
