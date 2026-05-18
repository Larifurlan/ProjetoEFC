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

    def notify_order_approved(
        self,
        customer_name,
        customer_type
    ):

        print(
            f"Email enviado para "
            f"{customer_name}: Pedido aprovado!"
        )

        if customer_type == 'vip':

            print(
                f"SMS enviado para "
                f"{customer_name}: Pedido aprovado!"
            )

    def notify_order_sent(
        self,
        customer_name
    ):

        print(
            f"Email enviado para "
            f"{customer_name}: Pedido enviado!"
        )

    def notify_order_delivered(
        self,
        customer_name,
        customer_type,
        total
    ):

        print(
            f"Email enviado para "
            f"{customer_name}: Pedido entregue!"
        )

        if customer_type == 'vip':

            points = int(total * 2)

            print(
                f"Cliente VIP ganhou "
                f"{points} pontos!"
            )

        elif customer_type == 'corporativo':

            points = int(total * 1.5)

            print(
                f"Cliente corporativo ganhou "
                f"{points} pontos!"
            )

        else:

            points = int(total)

            print(
                f"Cliente ganhou "
                f"{points} pontos!"
            )