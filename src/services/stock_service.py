from src.interfaces.services.stock_service_interface import (
    StockServiceInterface,
)


class StockService(StockServiceInterface):
    def validate_stock(self, items):

        stock = {
            'produto1': 100,
            'produto2': 50,
            'produto3': 75
        }

        for item in items:

            if item['nome'] not in stock:

                print(
                    f"Produto "
                    f"{item['nome']} "
                    f"nao encontrado!"
                )

                return False

            if stock[item['nome']] < item['q']:

                print(
                    f"Estoque insuficiente "
                    f"para {item['nome']}!"
                )

                return False

        return True