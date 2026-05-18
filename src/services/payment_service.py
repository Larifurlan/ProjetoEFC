from src.interfaces.services.payment_service_interface import (
    PaymentServiceInterface,
)


class PaymentService(PaymentServiceInterface):
    
    def process_payment(self, order, method, value):

        if not order:
            return False

        if value < order['tot']:

            print("Valor insuficiente!")

            return False

        if method == 'cartao':

            print("Processando pagamento com cartao...")
            print("Cartao validado!")

            return 'aprovado'

        elif method == 'pix':

            print("Gerando QR Code PIX...")
            print("PIX recebido!")

            return 'aprovado'

        elif method == 'boleto':

            print("Gerando boleto...")
            print("Boleto gerado!")

            return 'pendente'

        else:

            print("Metodo de pagamento invalido!")

            return False