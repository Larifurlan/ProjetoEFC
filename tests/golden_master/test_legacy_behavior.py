import os
import sys
from pathlib import Path

import pytest

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

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


def test_pedido_vip_aplica_desconto_de_5_por_cento(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Maria', itens, 'vip')

    pedido = sis.get_ped(id_ped)

    assert pedido['tot'] == pytest.approx(95.0)


def test_cliente_corporativo_recebe_desconto(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Empresa XYZ', itens, 'corporativo')

    pedido = sis.get_ped(id_ped)

    assert pedido['tot'] == pytest.approx(90.0)


def test_pagamento_insuficiente_falha(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao', itens, 'normal')

    assert sis.proc_pag(id_ped, 'cartao', 50) is False


def test_pix_aprova_pedido_automaticamente(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao', itens, 'normal')

    sis.proc_pag(id_ped, 'pix', 100)

    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'aprovado'


def test_boleto_nao_aprova_automaticamente(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao', itens, 'normal')

    sis.proc_pag(id_ped, 'boleto', 100)

    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'pendente'


def test_metodo_pagamento_invalido_retorna_false(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao', itens, 'normal')

    resultado = sis.proc_pag(id_ped, 'bitcoin', 100)

    assert resultado is False


def test_validar_estoque_retorna_true_para_produtos_validos(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    assert sis.validar_estoque(itens) is True


def test_validar_estoque_retorna_false_para_produto_inexistente(sis):
    itens = [
        {'nome': 'produto_invalido', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    assert sis.validar_estoque(itens) is False


def test_cancelar_pedido_altera_status_para_cancelado(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Carlos', itens, 'normal')

    sis.cancelar_pedido(id_ped)

    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'cancelado'


def test_upd_st_altera_status_para_enviado(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao', itens, 'normal')

    sis.upd_st(id_ped, 'enviado')

    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'enviado'


def test_upd_st_altera_status_para_entregue(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao', itens, 'normal')

    sis.upd_st(id_ped, 'entregue')

    pedido = sis.get_ped(id_ped)

    assert pedido['st'] == 'entregue'


def test_get_ped_retorna_none_para_id_inexistente(sis):
    assert sis.get_ped(9999) is None


def test_gerar_relatorio_vendas_cria_arquivo(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    sis.add_ped('Joao', itens, 'normal')

    sis.gerar_rel('vendas')

    arquivo = Path('rel_vendas.txt')

    assert arquivo.exists()

    conteudo = arquivo.read_text()

    assert 'Total de vendas' in conteudo


def test_gerar_relatorio_clientes_cria_arquivo(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    sis.add_ped('Maria', itens, 'vip')

    sis.gerar_rel('clientes')

    arquivo = Path('rel_clientes.txt')

    assert arquivo.exists()

    conteudo = arquivo.read_text()

    assert 'Maria' in conteudo


def test_cliente_vip_recebe_sms(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    sis.add_ped('Maria', itens, 'vip')

    saida = capsys.readouterr()

    assert 'SMS enviado para Maria' in saida.out


def test_cliente_corporativo_notifica_gerente(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    sis.add_ped('Empresa XYZ', itens, 'corporativo')

    saida = capsys.readouterr()

    assert 'gerente de conta' in saida.out


def test_ped_especial_cria_pedido_com_acrescimo(tmp_path, monkeypatch):
    from legacy import PedEspecial

    monkeypatch.chdir(tmp_path)

    ped = PedEspecial()

    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = ped.add_ped('Cliente Especial', itens, 'especial')

    pedido = ped.get_ped(id_ped)

    assert pedido['tot'] == pytest.approx(115.0)

    ped.close()


def test_ped_especial_upd_st(tmp_path, monkeypatch):
    from legacy import PedEspecial

    monkeypatch.chdir(tmp_path)

    ped = PedEspecial()

    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = ped.add_ped('Cliente Especial', itens, 'especial')

    ped.upd_st(id_ped, 'aprovado')

    pedido = ped.get_ped(id_ped)

    assert pedido['st'] == 'aprovado'

    ped.close()

def test_item_desc20_aplica_desconto_corretamente(sis):
    itens = [
        {'nome': 'produto3', 'p': 200, 'q': 1, 'tipo': 'desc20'}
    ]

    id_ped = sis.add_ped('Cliente', itens, 'normal')

    pedido = sis.get_ped(id_ped)

    assert pedido['tot'] == pytest.approx(160.0)


def test_item_frete_gratis_calcula_total(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'frete_gratis'}
    ]

    id_ped = sis.add_ped('Cliente', itens, 'normal')

    pedido = sis.get_ped(id_ped)

    assert pedido['tot'] == pytest.approx(200.0)


def test_pagamento_cartao_aprova_pedido(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao', itens, 'normal')

    resultado = sis.proc_pag(id_ped, 'cartao', 100)

    pedido = sis.get_ped(id_ped)

    assert resultado is True
    assert pedido['st'] == 'aprovado'


def test_cliente_normal_ganha_pontos_ao_entregar(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Joao', itens, 'normal')

    sis.upd_st(id_ped, 'entregue')

    saida = capsys.readouterr()

    assert 'Cliente ganhou' in saida.out


def test_cliente_vip_ganha_pontos_ao_entregar(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Maria', itens, 'vip')

    sis.upd_st(id_ped, 'entregue')

    saida = capsys.readouterr()

    assert 'Cliente VIP ganhou' in saida.out


def test_cliente_corporativo_ganha_pontos_ao_entregar(sis, capsys):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}
    ]

    id_ped = sis.add_ped('Empresa XYZ', itens, 'corporativo')

    sis.upd_st(id_ped, 'entregue')

    saida = capsys.readouterr()

    assert 'Cliente corporativo ganhou' in saida.out


def test_validar_estoque_retorna_false_para_estoque_insuficiente(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 999, 'tipo': 'normal'}
    ]

    assert sis.validar_estoque(itens) is False


def test_proc_pag_retorna_false_para_pedido_inexistente(sis):
    resultado = sis.proc_pag(9999, 'pix', 100)

    assert resultado is False