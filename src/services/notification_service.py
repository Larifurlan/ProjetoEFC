from src.interfaces.services.notification_service_interface import (
    NotificationServiceInterface,
)

class NotificationService(NotificationServiceInterface):
    def notify_new_order(self, customer_name, customer_type):

        if customer_type == 'normal':

            print(
                f"Email enviado para "
                f"{customer_name}: Pedido recebido!"
            )

        elif customer_type == 'vip':

            print(
                f"Email enviado para "
                f"{customer_name}: Pedido recebido!"
            )

            print(
                f"SMS enviado para "
                f"{customer_name}: Pedido VIP recebido!"
            )

        elif customer_type == 'corporativo':

            print(
                f"Email enviado para "
                f"{customer_name}: Pedido recebido!"
            )

            print(
                f"Notificacao enviada ao gerente "
                f"de conta de {customer_name}"
            )