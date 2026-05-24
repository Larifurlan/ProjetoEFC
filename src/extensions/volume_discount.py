from collections import defaultdict

from src.domain import OrderItem
from src.strategies.discount_strategy import OrderAdjustmentStrategy


class VolumeDiscountAdjustment(OrderAdjustmentStrategy):
    def apply(self, items: list[OrderItem], total: float) -> float:
        quantities: dict[str, int] = defaultdict(int)

        for item in items:
            quantities[item["nome"]] += item["q"]

        discount = 0.0

        for item in items:
            if quantities[item["nome"]] >= 3:
                discount += float(item["p"]) * item["q"] * 0.15

        return total - discount
