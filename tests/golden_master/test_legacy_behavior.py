import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from legacy import Sis


@pytest.fixture
def sis(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    s = Sis()
    yield s
    s.close()


def test_pedido_normal_calcula_total_corretamente(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'desc10'},
    ]

    id_ped = sis.add_ped('Joao Silva', itens, 'normal')

    pedido = sis.get_ped(id_ped)

    assert pedido['tot'] == pytest.approx(245.0)
    assert pedido['st'] == 'pendente'