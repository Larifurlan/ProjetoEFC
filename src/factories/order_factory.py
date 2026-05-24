from abc import ABC, abstractmethod

from src.domain import OrderDraft, OrderItem
from src.services.order_service import OrderService


class OrderFactory(ABC):
    @abstractmethod
    def create_order(
        self,
        client_name: str,
        items: list[OrderItem],
        customer_type: str,
    ) -> OrderDraft:
        raise NotImplementedError


class DefaultOrderFactory(OrderFactory):
    def __init__(self, order_service: OrderService | None = None) -> None:
        self.order_service = order_service or OrderService()

    def create_order(
        self,
        client_name: str,
        items: list[OrderItem],
        customer_type: str,
    ) -> OrderDraft:
        return OrderDraft(
            client_name=client_name,
            items=items,
            total=self.order_service.calculate_total(
                items,
                customer_type,
            ),
            status="pendente",
            date=self.order_service.generate_date(),
            customer_type=customer_type,
        )
