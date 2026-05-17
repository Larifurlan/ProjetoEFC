from abc import ABC, abstractmethod


class PaymentServiceInterface(ABC):

    @abstractmethod
    def process_payment(
        self,
        order,
        method,
        value
    ):
        pass