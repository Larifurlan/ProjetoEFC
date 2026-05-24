import os
import sys

import pytest

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../..",
        )
    )
)

from src.extensions import create_extended_sis


@pytest.fixture
def sis(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    service = create_extended_sis()
    yield service
    service.close()


def test_pagamento_crypto_aplica_taxa_de_dois_por_cento(sis):
    itens = [
        {"nome": "produto1", "p": 100, "q": 1, "tipo": "normal"},
    ]

    id_ped = sis.add_ped("Joao", itens, "normal")

    assert sis.proc_pag(id_ped, "crypto", 101.99) is False
    assert sis.proc_pag(id_ped, "crypto", 102) is True
    assert sis.get_ped(id_ped)["st"] == "aprovado"


def test_whatsapp_notifica_todos_os_tipos_de_cliente(sis, capsys):
    itens = [
        {"nome": "produto1", "p": 100, "q": 1, "tipo": "normal"},
    ]

    sis.add_ped("Empresa XYZ", itens, "corporativo")

    saida = capsys.readouterr()

    assert "WhatsApp enviado para Empresa XYZ" in saida.out


def test_desconto_progressivo_por_volume(sis):
    itens = [
        {"nome": "produto1", "p": 100, "q": 3, "tipo": "normal"},
    ]

    id_ped = sis.add_ped("Maria", itens, "normal")

    assert sis.get_ped(id_ped)["tot"] == pytest.approx(255.0)


def test_desconto_progressivo_soma_unidades_do_mesmo_item(sis):
    itens = [
        {"nome": "produto1", "p": 100, "q": 2, "tipo": "normal"},
        {"nome": "produto1", "p": 100, "q": 1, "tipo": "normal"},
    ]

    id_ped = sis.add_ped("Maria", itens, "normal")

    assert sis.get_ped(id_ped)["tot"] == pytest.approx(255.0)
