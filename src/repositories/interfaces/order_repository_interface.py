from abc import ABC, abstractmethod

from src.domain import DbOrderRow, OrderItem, OrderRecord


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def save_order(
        self,
        client_name: str,
        items: list[OrderItem],
        total: float,
        status: str,
        date: str,
        customer_type: str,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> OrderRecord | None:
        raise NotImplementedError

    @abstractmethod
    def update_status(self, order_id: int, status: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_orders_by_client(self, client_name: str) -> list[DbOrderRow]:
        raise NotImplementedError

    @abstractmethod
    def get_all_orders(self) -> list[DbOrderRow]:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
