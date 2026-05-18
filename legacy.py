from datetime import datetime

from src.services.payment_service import PaymentService
from src.repositories.order_repository import OrderRepository
from src.services.notification_service import NotificationService
from src.services.stock_service import StockService
from src.services.report_service import ReportService
from src.services.order_service import OrderService

from src.repositories.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)

from src.interfaces.services.payment_service_interface import (
    PaymentServiceInterface,
)

from src.interfaces.services.notification_service_interface import (
    NotificationServiceInterface,
)

from src.interfaces.services.stock_service_interface import (
    StockServiceInterface,
)

from src.interfaces.services.report_service_interface import (
    ReportServiceInterface,
)

class Sis:

    def __init__(
        self,
        repository: OrderRepositoryInterface = None,
        payment_service: PaymentServiceInterface = None,
        notification_service: NotificationServiceInterface = None,
        stock_service: StockServiceInterface = None,
        report_service: ReportServiceInterface = None,
        order_service: OrderService = None,
    ):

        self.repository = (
            repository or OrderRepository()
        )

        self.payment_service = (
            payment_service or PaymentService()
        )

        self.notification_service = (
            notification_service or NotificationService()
        )

        self.stock_service = (
            stock_service or StockService()
        )

        self.report_service = (
            report_service or ReportService()
        )

        self.order_service = (
            order_service or OrderService()
        )

    def add_ped(self, n, its, t):

        dt = self.order_service.generate_date()

        tot = self.order_service.calculate_total(
            its,
            t
        )

        order_id = self.repository.save_order(
            n,
            its,
            tot,
            'pendente',
            dt,
            t
        )

        self.notification_service.notify_new_order(
            n,
            t
        )

        return order_id

    def get_ped(self, id):
        return self.repository.get_order_by_id(id)

    def upd_st(self, id, s):

        p = self.get_ped(id)

        if p:

            self.repository.update_status(id, s)

            if s == 'aprovado':

                self.notification_service.notify_order_approved(
                    p['cli'],
                    p['tp']
                )

            elif s == 'enviado':

                self.notification_service.notify_order_sent(
                    p['cli']
                )

            elif s == 'entregue':

                self.notification_service.notify_order_delivered(
                    p['cli'],
                    p['tp'],
                    p['tot']
                )

    def calc_tot_cli(self, n):

        rs = self.repository.get_orders_by_client(n)

        t = 0

        for r in rs:
            t += r[3]

        return t

    def gerar_rel(self, tipo):

        orders = self.repository.get_all_orders()

        if tipo == 'vendas':

            self.report_service.generate_sales_report(
                orders
            )

        elif tipo == 'clientes':

            self.report_service.generate_clients_report(
                orders,
                self.calc_tot_cli
            )

    def proc_pag(self, id, m, vl):

        p = self.get_ped(id)

        result = self.payment_service.process_payment(
            p,
            m,
            vl
        )

        if result == 'aprovado':

            self.upd_st(id, 'aprovado')

            return True

        elif result == 'pendente':

            return True

        return False

    def validar_estoque(self, its):

        return self.stock_service.validate_stock(its)

    def cancelar_pedido(self, id):

        self.repository.update_status(id, 'cancelado')

        print(f"Pedido {id} cancelado")

    def close(self):
        self.repository.close()


class PedEspecial(Sis):

    def add_ped(self, n, its, t):

        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        tot = 0

        for i in its:

            if i['tipo'] == 'normal':
                tot += i['p'] * i['q']

            elif i['tipo'] == 'desc10':
                tot += i['p'] * i['q'] * 0.9

            elif i['tipo'] == 'desc20':
                tot += i['p'] * i['q'] * 0.8

        tot = tot * 1.15

        order_id = self.repository.save_order(
            n,
            its,
            tot,
            'pendente',
            dt,
            t
        )

        print(
            f"Email especial enviado para {n}: "
            f"Pedido especial recebido!"
        )

        return order_id

    def upd_st(self, id, s):

        p = self.get_ped(id)

        if p:

            self.repository.update_status(id, s)

            print(f"Pedido especial {id} -> {s}")