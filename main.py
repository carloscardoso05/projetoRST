import os
from typing import Dict

from prettytable import PrettyTable

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


def test_counting():
    for document, expected_counting in documents_counting.items():
        table = PrettyTable(["Relação", "Esperado", "Encontrado", "Resultado"])
        path = os.path.join(base_dir, document)
        reader = RS3Reader(path)
        print(f'\nTeste para {document}')
        counting = reader.count_relations()
        # df = pd.DataFrame.from_dict(counting, orient='index', columns=['encontrado'])
        # df = df.join(pd.DataFrame.from_dict(expected_counting, orient='index', columns=['esperado']))
        # df.replace(np.nan, 0, inplace=True)
        # df['resultado'] = df.apply(get_result, axis=1)
        # df['esperado'] = df['esperado'].astype(int)
        # df['encontrado'] = df['encontrado'].astype(int)
        for key in set(counting.keys()).union(expected_counting.keys()):
            esperado = expected_counting.get(key)
            encontrado = counting.get(key, 0)
            resultado = get_result(esperado, encontrado)
            table.add_row([key, esperado, encontrado, resultado])
        print(table.get_string(sortby="Resultado", reversesort=True))


if __name__ == '__main__':
    base_dir = 'documents'
    documents_counting: Dict[str, Dict[str, int]] = {
        'D1_C35_Folha_07-08-2007_14h11Paula.rs3': {
            'circumstance': 4,
            'same-unit': 3,
            'parenthetical': 4,
            'elaboration': 5,  # TODO rever contagem (só achei 3)
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
            'sequence': 4,
            'list': 3,
        },
        'D2_C34_Estadao_20-08-2007_13h22.rs3': {
            'circumstance': 1,
            'same-unit': 3,
            'parenthetical': 5,
            'elaboration': 6,
            'non-volitional-result': 2,
            'sequence': 1,
            'list': 2,
            'comparison': 1,
            'condition': 1,
            'attribution': 4,  # TODO rever contagem (só achei 3)
        },
        'D1_C44_Folha_19-09-2007_12h03.rs3': {
            'justify': 1,
            'same-unit': 4,
            'parenthetical': 5,
            'elaboration': 7,
            'volitional-cause': 1,
            'sequence': 3,
            'purpose': 4,
            'attribution': 6,  # TODO rever contagem (só achei 3)
            'concession': 1,
            'contrast': 1,
            'explanation': 3,
            'condition': 3,
        },
    }

    test_counting()
