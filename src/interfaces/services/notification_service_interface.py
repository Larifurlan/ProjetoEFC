from abc import ABC, abstractmethod


class NotificationServiceInterface(ABC):

    @abstractmethod
    def notify_new_order(
        self,
        customer_name,
        customer_type
    ):
        pass

    @abstractmethod
    def notify_order_approved(
        self,
        customer_name,
        customer_type
    ):
        pass

    @abstractmethod
    def notify_order_sent(
        self,
        customer_name
    ):
        pass

    @abstractmethod
    def notify_order_delivered(
        self,
        customer_name,
        customer_type,
        total
    ):
        pass