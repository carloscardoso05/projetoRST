import os
import re
from collections import Counter
from typing import List, Dict, cast
from xml.etree import ElementTree

from elements import Relation, Group, Segment, Signal, Node


def to_count(node: Node) -> bool:
    # Quando a relname de um nó é None, significa que é a raiz da árvore
    if node.relname == 'span' or node.relname is None: return False
    if node.is_multinuclear:
        if node.relname == 'same-unit':
            return node.siblings_of_same_relation[0] == node
        else:  # contrast, sequence ou list
            index = node.siblings_of_same_relation.index(node)
            if index + 1 == len(node.siblings_of_same_relation):
                return False
            node_on_right = node.siblings_of_same_relation[index + 1]
            return node.sentences == node_on_right.sentences
    return are_of_same_sentence(node.parent, node)


def are_of_same_sentence(*nodes: Node) -> bool:
    segments: List[Segment] = []
    for node in nodes:
        if isinstance(node, Group):
            segments.extend(node.get_all_segments())
        elif isinstance(node, Segment):
            segments.append(node)
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
            node.relation = self.relations.get(node.relname)
        for signal in self.signals.values():
            signal.source = self.nodes.get(signal.source_id)
            signal.source.signals.append(signal)

    def assing_sentences(self) -> None:
        sentence_id = 1
        initial_token_id = 1
        for segment in sorted(self.segments.values(), key=lambda s: cast(Segment, s).order):
            segment.sentence_id = sentence_id
            segment.initial_token_id = initial_token_id
            if re.match(r'.*[.? !]\s*[\'\"]?\s*', segment.tokens[-1]):
                sentence_id += 1
            initial_token_id += len(segment.tokens)

    @property
    def nodes(self) -> Dict[int, Node]:
        nodes = self.segments | self.groups
        return nodes

    def get_relations(self) -> Dict[str, Relation]:
        relations_elements = self.root.findall('header/relations/rel')
        relations = map(Relation.from_element, relations_elements)
        return {rel.name: rel for rel in relations}

    def get_groups(self) -> Dict[int, Group]:
        groups_elements = self.root.findall('body/group')
        groups: Dict[int, Group] = {}
        for group_element in groups_elements:
            group = Group.from_element(group_element)
            groups[group.id] = group
        return groups

    def get_segments(self) -> Dict[int, Segment]:
        segments_elements = self.root.findall('body/segment')
        segments: Dict[int, Segment] = {}
        order = 1
        for segment_element in segments_elements:
            segment = Segment.from_element(segment_element, order)
            segments[segment.id] = segment
            order += 1
        return segments

    def get_signals(self) -> Dict[int, Signal]:
        signals_elements = self.root.findall('body/signals/signal')
        signals = {i: Signal.from_element(signals_elements[i], i) for i in range(len(signals_elements))}
        return signals

    def count_relations(self) -> Dict[str, int]:
        nodes = filter(to_count, self.nodes.values())
        counting = dict(Counter(map(lambda node: node.relname, nodes)))
        return counting
