from abc import ABC, abstractmethod

from src.domain import OrderRecord, PaymentStatus


class PaymentStrategy(ABC):
    @abstractmethod
    def supports(self, method: str) -> bool:
        raise NotImplementedError

    def required_amount(self, order: OrderRecord) -> float:
        return order["tot"]

    @abstractmethod
    def process(self, order: OrderRecord, value: float) -> PaymentStatus:
        raise NotImplementedError


class CardPaymentStrategy(PaymentStrategy):
    def supports(self, method: str) -> bool:
        return method == "cartao"

    def process(self, order: OrderRecord, value: float) -> PaymentStatus:
        print("Processando pagamento com cartao...")
        print("Cartao validado!")
        return PaymentStatus.APPROVED


class PixPaymentStrategy(PaymentStrategy):
    def supports(self, method: str) -> bool:
        return method == "pix"

    def process(self, order: OrderRecord, value: float) -> PaymentStatus:
        print("Gerando QR Code PIX...")
        print("PIX recebido!")
        return PaymentStatus.APPROVED


class BoletoPaymentStrategy(PaymentStrategy):
    def supports(self, method: str) -> bool:
        return method == "boleto"

    def process(self, order: OrderRecord, value: float) -> PaymentStatus:
        print("Gerando boleto...")
        print("Boleto gerado!")
        return PaymentStatus.PENDING


def default_payment_strategies() -> list[PaymentStrategy]:
    return [
        CardPaymentStrategy(),
        PixPaymentStrategy(),
        BoletoPaymentStrategy(),
    ]
