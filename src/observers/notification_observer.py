from abc import ABC, abstractmethod
from dataclasses import dataclass

_EVENT_NEW_ORDER = "new_order"
_EVENT_APPROVED = "approved"
_EVENT_SENT = "sent"
_EVENT_DELIVERED = "delivered"


@dataclass(frozen=True)
class NotificationEvent:
    name: str
    customer_name: str = ""
    customer_type: str = ""
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
        _EVENT_NEW_ORDER: "Pedido recebido!",
        _EVENT_APPROVED: "Pedido aprovado!",
        _EVENT_SENT: "Pedido enviado!",
        _EVENT_DELIVERED: "Pedido entregue!",
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
            and event.name in {_EVENT_NEW_ORDER, _EVENT_APPROVED}
        )

    def update(self, event: NotificationEvent) -> None:
        if event.name == _EVENT_NEW_ORDER:
            print(
                f"SMS enviado para {event.customer_name}: "
                f"Pedido VIP recebido!"
            )

        print(
            f"SMS enviado para {event.customer_name}: "
            f"Pedido aprovado!"
        )


class AccountManagerNotificationObserver(NotificationObserver):
    def supports(self, event: NotificationEvent) -> bool:
        return (
            event.customer_type == "corporativo"
            and event.name == _EVENT_NEW_ORDER
        )

    def update(self, event: NotificationEvent) -> None:
        print(
            "Notificacao enviada ao gerente "
            f"de conta de {event.customer_name}"
        )


class LoyaltyPointsObserver(NotificationObserver):
    def supports(self, event: NotificationEvent) -> bool:
        return event.name == _EVENT_DELIVERED and event.total is not None

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
