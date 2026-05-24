from abc import ABC, abstractmethod


class NotificationServiceInterface(ABC):
    @abstractmethod
    def notify_new_order(
        self,
        customer_name: str,
        customer_type: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def notify_order_approved(
        self,
        customer_name: str,
        customer_type: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def notify_order_sent(
        self,
        customer_name: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def notify_order_delivered(
        self,
        customer_name: str,
        customer_type: str,
        total: float,
    ) -> None:
        raise NotImplementedError
