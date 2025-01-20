import numpy as np

from RS3Reader import RS3Reader
from collections import Counter
import pandas as pd

from elements import Segment

if __name__ == '__main__':
    file_path = r'documents/D1_C35_Folha_07-08-2007_14h11Paula.rs3'
    reader = RS3Reader(file_path)

    nodes = [node.relname for node in reader.nodes.values() if
             (isinstance(node, Segment) and not node.is_multinuclear)
             or (node.signals and node.relname in ["same-unit"])]

    counting = Counter(nodes)

    df_count = pd.DataFrame.from_dict(counting, orient='index', columns=['count'])

    expected = {
        'circumstance': 4,
        'same-unit': 4,
        'parenthetical': 4,
        'elaboration': 5,
        'attribution': 6,
        'volitional-cause': 5,
        'concession': 2,
        'list': 2,
        'purpose': 1,
        'evidence': 1,
    }

    df_expected = pd.DataFrame.from_dict(expected, orient='index', columns=['expected'])
    df = pd.concat([df_expected, df_count], axis=1)
    df.replace(np.nan, 0, inplace=True)
    print(df)
