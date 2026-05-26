from src.observers.notification_observer import NotificationObserver, NotificationEvent

class WhatsAppNotificationObserver(NotificationObserver):
    _messages = {
        "new_order": "Pedido recebido!",
        "approved": "Pedido aprovado!",
        "sent": "Pedido enviado!",
        "delivered": "Pedido entregue!",
    }

    def supports(self, event: NotificationEvent) -> bool:
        # Disponível para todos os clientes em eventos mapeados
        return event.name in self._messages

    def update(self, event: NotificationEvent) -> None:
        print(
            f"WhatsApp enviado para {event.customer_name}: "
            f"{self._messages[event.name]}"
        )
        