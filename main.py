import re

import numpy as np

from RS3Reader import RS3Reader, are_of_same_sentence
from collections import Counter
import pandas as pd

from typing import cast

from elements import Segment, Node

if __name__ == '__main__':
    file_path = r'documents/D1_C25_Folha_16-07-2007_07h50Paula.rs3'
    reader = RS3Reader(file_path)


    def to_count(node: Node) -> bool:
        if node.is_multinuclear:
            return len(node.signals) > 0
        return are_of_same_sentence(node.parent) and (isinstance(node, Segment) or node.signals)


    nodes = [node for node in reader.nodes.values() if to_count(node)]

    for node in nodes:
        if node.relname == 'elaboration':
            # print('id:', node.id, '| parent_id:', node.parent_id)
            print(node)

    counting = Counter(map(lambda node: node.relname, nodes))

    df = pd.DataFrame.from_dict(counting, orient='index', columns=['count'])
    df.replace(np.nan, 0, inplace=True)
    print(df)
