from legacy import Sis

from src.repositories.order_repository import OrderRepository
from src.services.payment_service import PaymentService
from src.services.notification_service import NotificationService
from src.services.stock_service import StockService
from src.services.report_service import ReportService
from src.services.order_service import OrderService


repository = OrderRepository()

payment_service = PaymentService()

notification_service = NotificationService()

stock_service = StockService()

report_service = ReportService()

order_service = OrderService()


sis = Sis(
    repository,
    payment_service,
    notification_service,
    stock_service,
    report_service,
    order_service,
)