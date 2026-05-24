from typing import Optional

from src.domain import OrderItem, OrderRecord, PaymentStatus
from src.factories.order_factory import DefaultOrderFactory, OrderFactory
from src.interfaces.services.notification_service_interface import (
    NotificationServiceInterface,
)
from src.interfaces.services.payment_service_interface import (
    PaymentServiceInterface,
)
from src.interfaces.services.report_service_interface import (
    ReportServiceInterface,
)
from src.interfaces.services.stock_service_interface import (
    StockServiceInterface,
)
from src.repositories.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)
from src.repositories.order_repository import OrderRepository
from src.services.notification_service import NotificationService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService
from src.services.report_service import ReportService
from src.services.stock_service import StockService
from src.strategies.discount_strategy import (
    CustomerTypeDiscountStrategy,
    default_customer_discount_strategies,
)


class Sis:
    def __init__(
        self,
        repository: Optional[OrderRepositoryInterface] = None,
        payment_service: Optional[PaymentServiceInterface] = None,
        notification_service: Optional[
            NotificationServiceInterface
        ] = None,
        stock_service: Optional[StockServiceInterface] = None,
        report_service: Optional[ReportServiceInterface] = None,
        order_factory: Optional[OrderFactory] = None,
    ) -> None:
        self.repository = repository or OrderRepository()
        self.payment_service = payment_service or PaymentService()
        self.notification_service = (
            notification_service or NotificationService()
        )
        self.stock_service = stock_service or StockService()
        self.report_service = report_service or ReportService()
        self.order_factory = order_factory or DefaultOrderFactory()

    def add_ped(self, n: str, its: list[OrderItem], t: str) -> int:
        order = self.order_factory.create_order(n, its, t)

        order_id = self.repository.save_order(
            order.client_name,
            order.items,
            order.total,
            order.status,
            order.date,
            order.customer_type,
        )

        self.notification_service.notify_new_order(n, t)

        return order_id

    def get_ped(self, id: int) -> OrderRecord | None:
        return self.repository.get_order_by_id(id)

    def upd_st(self, id: int, s: str) -> None:
        p = self.get_ped(id)

        if p:
            self.repository.update_status(id, s)

            if s == "aprovado":
                self.notification_service.notify_order_approved(
                    p["cli"],
                    p["tp"],
                )

            elif s == "enviado":
                self.notification_service.notify_order_sent(p["cli"])

            elif s == "entregue":
                self.notification_service.notify_order_delivered(
                    p["cli"],
                    p["tp"],
                    p["tot"],
                )

    def calc_tot_cli(self, n: str) -> float:
        rs = self.repository.get_orders_by_client(n)
        total = 0.0

        for r in rs:
            total += r[3]

        return total

    def gerar_rel(self, tipo: str) -> None:
        orders = self.repository.get_all_orders()

        if tipo == "vendas":
            self.report_service.generate_sales_report(orders)

        elif tipo == "clientes":
            self.report_service.generate_clients_report(
                orders,
                self.calc_tot_cli,
            )

    def proc_pag(self, id: int, m: str, vl: float) -> bool:
        p = self.get_ped(id)

        result = self.payment_service.process_payment(p, m, vl)

        if result is PaymentStatus.APPROVED:
            self.upd_st(id, "aprovado")
            return True

        if result is PaymentStatus.PENDING:
            return True

        return False

    def validar_estoque(self, its: list[OrderItem]) -> bool:
        return self.stock_service.validate_stock(its)

    def cancelar_pedido(self, id: int) -> None:
        self.repository.update_status(id, "cancelado")
        print(f"Pedido {id} cancelado")

    def close(self) -> None:
        self.repository.close()


class PedEspecial:
    def __init__(
        self,
        repository: Optional[OrderRepositoryInterface] = None,
    ) -> None:
        customer_strategies = default_customer_discount_strategies()
        customer_strategies.append(
            CustomerTypeDiscountStrategy("especial", 1.15)
        )
        order_service = OrderService(
            customer_discount_strategies=customer_strategies,
        )
        self._sis = Sis(
            repository=repository,
            notification_service=NotificationService([]),
            order_factory=DefaultOrderFactory(order_service),
        )

    def add_ped(self, n: str, its: list[OrderItem], t: str) -> int:
        order_id = self._sis.add_ped(n, its, t)
        print(f"Email especial enviado para {n}: Pedido especial recebido!")
        return order_id

    def get_ped(self, id: int) -> OrderRecord | None:
        return self._sis.get_ped(id)

    def upd_st(self, id: int, s: str) -> None:
        if self.get_ped(id):
            self._sis.repository.update_status(id, s)
            print(f"Pedido especial {id} -> {s}")

    def close(self) -> None:
        self._sis.close()
