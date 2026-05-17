from abc import ABC, abstractmethod


class ReportServiceInterface(ABC):

    @abstractmethod
    def generate_sales_report(self, orders):
        pass

    @abstractmethod
    def generate_clients_report(
        self,
        orders,
        calculate_total_client
    ):
        pass