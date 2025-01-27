import os
import unittest
from typing import Dict

import numpy as np
import pandas as pd

from RS3Reader import RS3Reader


class TestCounting(unittest.TestCase):
    base_dir = 'documents'
    documents_counting: Dict[str, Dict[str, int]] = {
        'D1_C35_Folha_07-08-2007_14h11Paula.rs3': {
            'circumstance': 4,
            'same-unit': 3,
            'parenthetical': 4,
            'elaboration': 5,
            'attribution': 6,
            'volitional-cause': 5,
            'concession': 2,
            'list': 2,
            'purpose': 1,
            'evidence': 0,
        },
        'D1_C25_Folha_16-07-2007_07h50Paula.rs3': {
            'circumstance': 3,
            'same-unit': 4,
            'parenthetical': 3,
            'elaboration': 10,
            'non-volitional-cause': 1,
            'purpose': 1,
            'sequence': 5,
            'list': 3,
        },
    }

    def test_counting(self):
        self.maxDiff = None
        for document, expected_counting in self.documents_counting.items():
            path = os.path.join(self.base_dir, document)
            reader = RS3Reader(path)
            print(f'\nTeste para {document}')
            counting = reader.count_relations()
            df = pd.DataFrame.from_dict(counting, orient='index', columns=['count'])
            df = df.join(pd.DataFrame.from_dict(expected_counting, orient='index', columns=['expected']))
            df.dropna(subset=['expected'], inplace=True)
            df['expected'] = pd.to_numeric(df['expected'], errors='coerce', downcast='integer')
            df['resultado'] = df.apply(
                lambda row: '✅' if row['count'] == row['expected'] else '❌', axis=1)
            print(df)


if __name__ == '__main__':
    unittest.main()
