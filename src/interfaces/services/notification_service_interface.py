from abc import ABC, abstractmethod


class NotificationServiceInterface(ABC):

    @abstractmethod
    def notify_new_order(
        self,
        customer_name,
        customer_type
    ):
        pass