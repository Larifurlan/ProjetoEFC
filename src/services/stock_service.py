from src.domain import OrderItem
from src.interfaces.services.stock_service_interface import (
    StockServiceInterface,
)

_DEFAULT_STOCK = {
    "produto1": 100,
    "produto2": 50,
    "produto3": 75,
}


class StockService(StockServiceInterface):
    def validate_stock(self, items: list[OrderItem]) -> bool:
        for item in items:
            product_name = item["nome"]

            if product_name not in _DEFAULT_STOCK:
                print(f"Produto {product_name} nao encontrado!")
                return False

            if _DEFAULT_STOCK[product_name] < item["q"]:
                print(f"Estoque insuficiente para {product_name}!")
                return False

        return True