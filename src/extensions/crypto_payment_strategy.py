from src.domain import OrderRecord, PaymentStatus
from src.strategies.payment_strategy import PaymentStrategy

class CryptoPaymentStrategy(PaymentStrategy):
    def supports(self, method: str) -> bool:
        return method == "criptomoeda"

    def required_amount(self, order: OrderRecord) -> float:
        # Aplica a taxa de 2% sobre o valor total do pedido
        return order["tot"] * 1.02

    def process(self, order: OrderRecord, value: float) -> PaymentStatus:
        print("Processando pagamento em criptomoeda...")
        print("Transferência na blockchain confirmada!")
        return PaymentStatus.APPROVED