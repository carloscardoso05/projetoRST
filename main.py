from RS3Reader import RS3Reader
from collections import Counter
import pandas as pd

from elements import Segment

if __name__ == '__main__':
    file_path = r'documents/D1_C35_Folha_07-08-2007_14h11Paula.rs3'
    reader = RS3Reader(file_path)

    counting = Counter([node.relname for node in reader.nodes.values() if isinstance(node, Segment) or any([signal.type != "CDP" for signal in node.signals])])
    df = pd.DataFrame.from_dict(counting, orient='index')
    print(df)
