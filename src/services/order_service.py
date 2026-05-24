from datetime import datetime

from src.domain import OrderItem
from src.strategies.discount_strategy import (
    CustomerDiscountStrategy,
    ItemDiscountStrategy,
    OrderAdjustmentStrategy,
    default_customer_discount_strategies,
    default_item_discount_strategies,
)


class OrderService:
    def __init__(
        self,
        item_discount_strategies: list[ItemDiscountStrategy] | None = None,
        customer_discount_strategies: (
            list[CustomerDiscountStrategy] | None
        ) = None,
        adjustment_strategies: list[OrderAdjustmentStrategy] | None = None,
    ) -> None:
        self.item_discount_strategies = (
            item_discount_strategies
            if item_discount_strategies is not None
            else default_item_discount_strategies()
        )
        self.customer_discount_strategies = (
            customer_discount_strategies
            if customer_discount_strategies is not None
            else default_customer_discount_strategies()
        )
        self.adjustment_strategies = adjustment_strategies or []

    def calculate_total(
        self,
        items: list[OrderItem],
        customer_type: str,
    ) -> float:
        total = sum(self._calculate_item_total(item) for item in items)

        for adjustment in self.adjustment_strategies:
            total = adjustment.apply(items, total)

        for customer_strategy in self.customer_discount_strategies:
            if customer_strategy.supports(customer_type):
                return customer_strategy.apply(total)

        return total

    def generate_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _calculate_item_total(self, item: OrderItem) -> float:
        for strategy in self.item_discount_strategies:
            if strategy.supports(item):
                return strategy.calculate(item)

        return 0.0
