from datetime import datetime


class OrderService:

    def calculate_total(self, items, customer_type):

        total = 0

        for item in items:

            if item['tipo'] == 'normal':

                total += item['p'] * item['q']

            elif item['tipo'] == 'desc10':

                total += item['p'] * item['q'] * 0.9

            elif item['tipo'] == 'desc20':

                total += item['p'] * item['q'] * 0.8

            elif item['tipo'] == 'frete_gratis':

                total += item['p'] * item['q']

        if customer_type == 'vip':

            total *= 0.95

        elif customer_type == 'corporativo':

            total *= 0.90

        return total

    def generate_date(self):

        return datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )