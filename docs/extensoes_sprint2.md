# Extensoes obrigatorias

As extensoes foram adicionadas sem alterar classes existentes. A ativacao fica
em `src/extensions/sprint2.py`, que compoe a aplicacao via injecao de
dependencias.

## Pagamento em criptomoeda

- Arquivo novo: `src/extensions/crypto_payment.py`
- Classe: `CryptoPaymentStrategy`
- Regra: aceita `crypto` ou `criptomoeda` e exige `total * 1.02`.

## Canal WhatsApp

- Arquivo novo: `src/extensions/whatsapp_notification.py`
- Classe: `WhatsAppNotificationObserver`
- Regra: observa eventos de pedido e envia mensagem para qualquer tipo de
  cliente.

## Desconto progressivo por volume

- Arquivo novo: `src/extensions/volume_discount.py`
- Classe: `VolumeDiscountAdjustment`
- Regra: quando a soma de unidades do mesmo item chega a 3 ou mais, aplica
  15% de desconto adicional sobre essas unidades.

## Testes

- Arquivo novo: `tests/unit/test_sprint2_extensions.py`
- Cobre crypto com taxa de 2%, WhatsApp para cliente corporativo e desconto
  por volume em linha unica ou linhas separadas do mesmo item.
