import os
from typing import List

import pandas as pd

from RS3Reader import RS3Reader


def get_result(esperado: int | None, encontrado: int) -> str:
    if esperado is None:
        return 'Não esperado'
    if encontrado is None:
        encontrado = 0
    if encontrado == esperado:
        return 'Ok'
    diff = int(esperado - encontrado)
    return 'Esperava %s ocorrências' % (f'+{diff}' if diff > 0 else diff)


def count_relations(documents: List[str]):
    with pd.ExcelWriter('resultados.xlsx', engine='xlsxwriter') as writer:
        df = pd.DataFrame()
        for path in documents:
            try:
                file_name = os.path.basename(path)
                reader = RS3Reader(path)
                counting = reader.count_relations()
                df = pd.concat([df, pd.DataFrame(counting, index=[file_name])])
            except Exception as e:
                print(f'Exception on document {path}')
                raise e
        df.fillna(0, inplace=True)
        df.to_excel(writer)


def main():
    base_dir = '../assets/somente rst'
    documents = [os.path.join(base_dir, document) for document in os.listdir(base_dir)]
    count_relations(documents)


if __name__ == '__main__':
    main()
