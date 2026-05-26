from src.strategies.discount_strategy import OrderAdjustmentStrategy
from src.domain import OrderItem

class VolumeDiscountAdjustmentStrategy(OrderAdjustmentStrategy):
    def apply(self, items: list[OrderItem], total: float) -> float:
        discount = 0.0
        for item in items:
            if item["q"] >= 3:
                # 15% de desconto adicional sobre o valor base deste item específico
                item_base_total = float(item["p"]) * item["q"]
                discount += item_base_total * 0.15
                
        return total - discount