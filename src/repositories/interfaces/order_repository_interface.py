from abc import ABC, abstractmethod


class OrderRepositoryInterface(ABC):

    @abstractmethod
    def save_order(
        self,
        client_name,
        items,
        total,
        status,
        date,
        customer_type
    ):
        pass

    @abstractmethod
    def get_order_by_id(self, order_id):
        pass

    @abstractmethod
    def update_status(self, order_id, status):
        pass

    @abstractmethod
    def get_orders_by_client(self, client_name):
        pass

    @abstractmethod
    def get_all_orders(self):
        pass