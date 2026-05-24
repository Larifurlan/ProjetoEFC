from src.domain import OrderRecord, PaymentStatus
from src.interfaces.services.payment_service_interface import (
    PaymentServiceInterface,
)
from src.strategies.payment_strategy import (
    PaymentStrategy,
    default_payment_strategies,
)


class PaymentService(PaymentServiceInterface):
    def __init__(
        self,
        strategies: list[PaymentStrategy] | None = None,
    ) -> None:
        self.strategies = (
            strategies
            if strategies is not None
            else default_payment_strategies()
        )

    def process_payment(
        self,
        order: OrderRecord | None,
        method: str,
        value: float,
    ) -> PaymentStatus:
        if not order:
            return PaymentStatus.REJECTED

        strategy = self._find_strategy(method)

        if strategy is None:
            print("Metodo de pagamento invalido!")
            return PaymentStatus.REJECTED

        if value < strategy.required_amount(order):
            print("Valor insuficiente!")
            return PaymentStatus.REJECTED

        return strategy.process(order, value)

    def _find_strategy(self, method: str) -> PaymentStrategy | None:
        for strategy in self.strategies:
            if strategy.supports(method):
                return strategy

        return None
