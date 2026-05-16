from datetime import datetime
from src.services.payment_service import PaymentService
from src.repositories.order_repository import OrderRepository
from src.services.notification_service import (
    NotificationService
)

from src.services.stock_service import StockService
from src.services.report_service import ReportService
from src.services.order_service import OrderService

class Sis:

    def __init__(self):
        self.repository = OrderRepository()
        self.stock_service = StockService()
        self.notification_service = NotificationService()
        self.payment_service = PaymentService()
        self.report_service = ReportService()
        self.order_service = OrderService()

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

                print(f"Email enviado para {p['cli']}: Pedido aprovado!")

                if p['tp'] == 'vip':
                    print(f"SMS enviado para {p['cli']}: Pedido aprovado!")

            elif s == 'enviado':

                print(f"Email enviado para {p['cli']}: Pedido enviado!")

            elif s == 'entregue':

                print(f"Email enviado para {p['cli']}: Pedido entregue!")

                if p['tp'] == 'vip':

                    pts = int(p['tot'] * 2)

                    print(f"Cliente VIP ganhou {pts} pontos!")

                elif p['tp'] == 'corporativo':

                    pts = int(p['tot'] * 1.5)

                    print(f"Cliente corporativo ganhou {pts} pontos!")

                else:

                    pts = int(p['tot'])

                    print(f"Cliente ganhou {pts} pontos!")

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