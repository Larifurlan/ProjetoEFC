from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain import OrderItem


class ItemDiscountStrategy(ABC):
    @abstractmethod
    def supports(self, item: OrderItem) -> bool:
        raise NotImplementedError

    @abstractmethod
    def calculate(self, item: OrderItem) -> float:
        raise NotImplementedError


class CustomerDiscountStrategy(ABC):
    @abstractmethod
    def supports(self, customer_type: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(self, total: float) -> float:
        raise NotImplementedError


class OrderAdjustmentStrategy(ABC):
    @abstractmethod
    def apply(self, items: list[OrderItem], total: float) -> float:
        raise NotImplementedError


@dataclass(frozen=True)
class ItemTypeDiscountStrategy(ItemDiscountStrategy):
    item_type: str
    multiplier: float

    def supports(self, item: OrderItem) -> bool:
        return item["tipo"] == self.item_type

    def calculate(self, item: OrderItem) -> float:
        return float(item["p"]) * item["q"] * self.multiplier


@dataclass(frozen=True)
class CustomerTypeDiscountStrategy(CustomerDiscountStrategy):
    customer_type: str
    multiplier: float

    def supports(self, customer_type: str) -> bool:
        return customer_type == self.customer_type

    def apply(self, total: float) -> float:
        return total * self.multiplier


def default_item_discount_strategies() -> list[ItemDiscountStrategy]:
    return [
        ItemTypeDiscountStrategy("normal", 1.0),
        ItemTypeDiscountStrategy("desc10", 0.9),
        ItemTypeDiscountStrategy("desc20", 0.8),
        ItemTypeDiscountStrategy("frete_gratis", 1.0),
    ]


def default_customer_discount_strategies() -> list[CustomerDiscountStrategy]:
    return [
        CustomerTypeDiscountStrategy("vip", 0.95),
        CustomerTypeDiscountStrategy("corporativo", 0.90),
    ]
