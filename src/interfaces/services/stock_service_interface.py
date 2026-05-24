from abc import ABC, abstractmethod

from src.domain import OrderItem


class StockServiceInterface(ABC):
    @abstractmethod
    def validate_stock(self, items: list[OrderItem]) -> bool:
        raise NotImplementedError
