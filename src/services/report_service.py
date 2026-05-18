from src.interfaces.services.report_service_interface import (
    ReportServiceInterface,
)


class ReportService(ReportServiceInterface):
    def generate_sales_report(self, orders):

        print("=== RELATORIO DE VENDAS ===")

        total_general = 0

        for order in orders:

            print(
                f"Pedido #{order[0]} - "
                f"Cliente: {order[1]} - "
                f"Total: R${order[3]:.2f} - "
                f"Status: {order[4]}"
            )

            total_general += order[3]

        print(f"Total Geral: R${total_general:.2f}")

        with open('rel_vendas.txt', 'w') as file:

            file.write(f"Total de vendas: {total_general}")

    def generate_clients_report(
        self,
        orders,
        calculate_total_client
    ):

        clients = {}

        for order in orders:

            name = order[1]
            customer_type = order[6]

            clients[name] = customer_type

        print("=== RELATORIO DE CLIENTES ===")

        with open('rel_clientes.txt', 'w') as file:

            for name, customer_type in clients.items():

                total = calculate_total_client(name)

                print(
                    f"Cliente: {name} "
                    f"({customer_type}) - "
                    f"Total gasto: R${total:.2f}"
                )

                file.write(f"{name},{customer_type}\n")