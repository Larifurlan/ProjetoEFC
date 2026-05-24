from abc import ABC, abstractmethod

from src.domain import OrderRecord, PaymentStatus


class PaymentServiceInterface(ABC):
    @abstractmethod
    def process_payment(
        self,
        order: OrderRecord | None,
        method: str,
        value: float,
    ) -> PaymentStatus:
        raise NotImplementedError
