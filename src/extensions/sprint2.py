from legacy import Sis
from src.extensions.crypto_payment import CryptoPaymentStrategy
from src.extensions.volume_discount import VolumeDiscountAdjustment
from src.extensions.whatsapp_notification import WhatsAppNotificationObserver
from src.factories.order_factory import DefaultOrderFactory
from src.observers.notification_observer import default_notification_observers
from src.repositories.interfaces.order_repository_interface import (
    OrderRepositoryInterface,
)
from src.repositories.order_repository import OrderRepository
from src.services.notification_service import NotificationService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService
from src.services.report_service import ReportService
from src.services.stock_service import StockService
from src.strategies.payment_strategy import default_payment_strategies


def create_extended_sis(
    repository: OrderRepositoryInterface | None = None,
) -> Sis:
    order_service = OrderService(
        adjustment_strategies=[VolumeDiscountAdjustment()]
    )
    payment_strategies = default_payment_strategies()
    payment_strategies.append(CryptoPaymentStrategy())

    observers = default_notification_observers()
    observers.append(WhatsAppNotificationObserver())

    return Sis(
        repository or OrderRepository(),
        PaymentService(payment_strategies),
        NotificationService(observers),
        StockService(),
        ReportService(),
        DefaultOrderFactory(order_service),
    )
