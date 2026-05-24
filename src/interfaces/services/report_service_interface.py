from abc import ABC, abstractmethod

from src.domain import CalculateTotalClient, DbOrderRow


class ReportServiceInterface(ABC):
    @abstractmethod
    def generate_sales_report(self, orders: list[DbOrderRow]) -> None:
        raise NotImplementedError

    @abstractmethod
    def generate_clients_report(
        self,
        orders: list[DbOrderRow],
        calculate_total_client: CalculateTotalClient,
    ) -> None:
        raise NotImplementedError
