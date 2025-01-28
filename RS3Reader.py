import itertools
import os
import re
from collections import Counter
from typing import List, Dict, cast
from xml.etree import ElementTree

from elements import Relation, Group, Segment, Signal, Node


def to_count(node: Node) -> bool:
    if node.is_multinuclear:
        return len(node.signals) > 0
    return isinstance(node, Segment) or (len(node.signals) > 0 and are_of_same_sentence(node.parent))


def are_of_same_sentence(*nodes: Node) -> bool:
    segments: List[Segment] = list(itertools.chain.from_iterable(
        [node.get_all_segments() for node in nodes if node is not None]))
    if len(segments) <= 1: return True
    sentence_id = segments[0].sentence_id
    for segment in segments[1:]:
        if sentence_id != segment.sentence_id:
            return False
    return True


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
        self.assing_sentences()

    def _link_nodes(self):
        for node in self.nodes.values():
            node.parent = self.nodes.get(node.parent_id)
            if node.parent is not None:
                node.parent.children.append(node)
        for signal in self.signals.values():
            signal.source = self.nodes.get(signal.source_id)
            signal.source.signals.append(signal)

    def assing_sentences(self) -> None:
        sentence_id = 1
        initial_token_id = 1
        for segment in sorted(self.segments.values(), key=lambda s: cast(Segment, s).id):
            segment.sentence_id = sentence_id
            segment.initial_token_id = initial_token_id
            if re.match(r'\.\s*[\'\"]?\s*', segment.tokens[-1]):
                sentence_id += 1
            initial_token_id += len(segment.tokens)

    def get_left_segment(self, segment: Segment) -> Segment | None:
        return self.segments.get(segment.id - 1)

    def get_right_segment(self, segment: Segment) -> Segment | None:
        return self.segments.get(segment.id + 1)

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

    def count_relations(self) -> Dict[str, int]:

        nodes = filter(to_count, self.nodes.values())

        counting = dict(Counter(map(lambda node: node.relname, nodes)))

        return counting
