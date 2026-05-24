from src.domain import OrderRecord, PaymentStatus
from src.strategies.payment_strategy import PaymentStrategy


class CryptoPaymentStrategy(PaymentStrategy):
    def supports(self, method: str) -> bool:
        return method in {"crypto", "criptomoeda"}

    def required_amount(self, order: OrderRecord) -> float:
        return order["tot"] * 1.02

    def process(self, order: OrderRecord, value: float) -> PaymentStatus:
        print("Processando pagamento em criptomoeda...")
        print("Taxa crypto de 2% aplicada.")
        return PaymentStatus.APPROVED
