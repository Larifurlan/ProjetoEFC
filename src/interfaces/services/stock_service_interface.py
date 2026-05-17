from abc import ABC, abstractmethod


class StockServiceInterface(ABC):

    @abstractmethod
    def validate_stock(self, items):
        pass