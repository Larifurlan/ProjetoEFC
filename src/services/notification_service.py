from src.interfaces.services.notification_service_interface import (
    NotificationServiceInterface,
)
from src.observers.notification_observer import (
    NotificationEvent,
    NotificationObserver,
    default_notification_observers,
)


class NotificationService(NotificationServiceInterface):
    def __init__(
        self,
        observers: list[NotificationObserver] | None = None,
    ) -> None:
        self.observers = (
            observers
            if observers is not None
            else default_notification_observers()
        )

    def notify_new_order(
        self,
        customer_name: str,
        customer_type: str,
    ) -> None:
        self._notify(
            NotificationEvent("new_order", customer_name, customer_type)
        )

    def notify_order_approved(
        self,
        customer_name: str,
        customer_type: str,
    ) -> None:
        self._notify(
            NotificationEvent("approved", customer_name, customer_type)
        )

    def notify_order_sent(
        self,
        customer_name: str,
    ) -> None:
        self._notify(NotificationEvent("sent", customer_name, ""))

    def notify_order_delivered(
        self,
        customer_name: str,
        customer_type: str,
        total: float,
    ) -> None:
        self._notify(
            NotificationEvent(
                "delivered",
                customer_name,
                customer_type,
                total,
            )
        )

    def _notify(self, event: NotificationEvent) -> None:
        for observer in self.observers:
            if observer.supports(event):
                observer.update(event)
