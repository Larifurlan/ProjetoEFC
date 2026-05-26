import os
import sys
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
from src.services.payment_service import PaymentService
from src.services.notification_service import NotificationService
from src.services.order_service import OrderService
from src.factories.order_factory import DefaultOrderFactory
from src.strategies.payment_strategy import default_payment_strategies
from src.observers.notification_observer import default_notification_observers

from src.extensions.crypto_payment_strategy import CryptoPaymentStrategy
from src.extensions.whatsapp_notification_observer import WhatsAppNotificationObserver
from src.extensions.volume_discount_strategy import VolumeDiscountAdjustmentStrategy
@pytest.fixture
def sis_ext(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    
    # Setup respeitando estritamente o OCP (apenas injeção)
    payment_strategies = default_payment_strategies()
    payment_strategies.append(CryptoPaymentStrategy())
    
    notif_observers = default_notification_observers()
    notif_observers.append(WhatsAppNotificationObserver())
    
    order_service = OrderService(
        adjustment_strategies=[VolumeDiscountAdjustmentStrategy()]
    )
    
    s = Sis(
        payment_service=PaymentService(strategies=payment_strategies),
        notification_service=NotificationService(observers=notif_observers),
        order_factory=DefaultOrderFactory(order_service=order_service)
    )
    yield s
    s.close()

def test_pagamento_criptomoeda_exige_taxa_de_2_porcento(sis_ext):
    itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis_ext.add_ped('Alice', itens, 'normal')
    
    # Valor base do pedido é 100. Taxa de 2% exige 102.
    # Tentar pagar sem a taxa deve falhar
    assert sis_ext.proc_pag(id_ped, 'criptomoeda', 100) is False
    
    # Pagar o valor correto com a taxa deve aprovar
    assert sis_ext.proc_pag(id_ped, 'criptomoeda', 102) is True
    
    pedido = sis_ext.get_ped(id_ped)
    assert pedido['st'] == 'aprovado'

def test_notificacao_whatsapp_enviada_em_novo_pedido(sis_ext, capsys):
    itens = [{'nome': 'produto1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    sis_ext.add_ped('Bruno', itens, 'normal')
    
    saida = capsys.readouterr()
    assert 'WhatsApp enviado para Bruno: Pedido recebido!' in saida.out

def test_desconto_progressivo_volume_acima_de_3_unidades(sis_ext):
    # 3 unidades a 100 cada = 300 base
    itens = [{'nome': 'produto1', 'p': 100, 'q': 3, 'tipo': 'normal'}]
    id_ped = sis_ext.add_ped('Carlos', itens, 'normal')
    
    pedido = sis_ext.get_ped(id_ped)
    
    # Total esperado: 300 - 15% (45) = 255.0
    assert pedido['tot'] == pytest.approx(255.0)

def test_sem_desconto_volume_para_menos_de_3_unidades(sis_ext):
    # 2 unidades a 100 cada = 200 base
    itens = [{'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'}]
    id_ped = sis_ext.add_ped('Diana', itens, 'normal')
    
    pedido = sis_ext.get_ped(id_ped)
    
    # Não deve haver desconto de 15%. Total esperado = 200.0
    assert pedido['tot'] == pytest.approx(200.0)