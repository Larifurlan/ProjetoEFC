from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationEvent:
    name: str
    customer_name: str
    customer_type: str
    total: float | None = None


class NotificationObserver(ABC):
    @abstractmethod
    def supports(self, event: NotificationEvent) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, event: NotificationEvent) -> None:
        raise NotImplementedError


class EmailNotificationObserver(NotificationObserver):
    _messages = {
        "new_order": "Pedido recebido!",
        "approved": "Pedido aprovado!",
        "sent": "Pedido enviado!",
        "delivered": "Pedido entregue!",
    }

    def supports(self, event: NotificationEvent) -> bool:
        return event.name in self._messages

    def update(self, event: NotificationEvent) -> None:
        print(
            f"Email enviado para {event.customer_name}: "
            f"{self._messages[event.name]}"
        )


class VipSmsNotificationObserver(NotificationObserver):
    def supports(self, event: NotificationEvent) -> bool:
        return (
            event.customer_type == "vip"
            and event.name in {"new_order", "approved"}
        )

    def update(self, event: NotificationEvent) -> None:
        if event.name == "new_order":
            print(
                f"SMS enviado para {event.customer_name}: "
                f"Pedido VIP recebido!"
            )
            return

        print(
            f"SMS enviado para {event.customer_name}: "
            f"Pedido aprovado!"
        )


class AccountManagerNotificationObserver(NotificationObserver):
    def supports(self, event: NotificationEvent) -> bool:
        return (
            event.customer_type == "corporativo"
            and event.name == "new_order"
        )

    def update(self, event: NotificationEvent) -> None:
        print(
            "Notificacao enviada ao gerente "
            f"de conta de {event.customer_name}"
        )


class LoyaltyPointsObserver(NotificationObserver):
    def supports(self, event: NotificationEvent) -> bool:
        return event.name == "delivered" and event.total is not None

    def update(self, event: NotificationEvent) -> None:
        total = event.total or 0.0

        if event.customer_type == "vip":
            points = int(total * 2)
            print(f"Cliente VIP ganhou {points} pontos!")
            return

        if event.customer_type == "corporativo":
            points = int(total * 1.5)
            print(f"Cliente corporativo ganhou {points} pontos!")
            return

        points = int(total)
        print(f"Cliente ganhou {points} pontos!")


def default_notification_observers() -> list[NotificationObserver]:
    return [
        EmailNotificationObserver(),
        VipSmsNotificationObserver(),
        AccountManagerNotificationObserver(),
        LoyaltyPointsObserver(),
    ]
