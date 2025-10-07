import asyncio
from typing import Dict, Any

from models import (
    NotificationRequest,
    UserContact,
    NotificationPriority,
    NotificationType,
)
from providers import EmailProvider, SMSProvider, TelegramProvider
from prioritization import PriorityManager
from health import (
    HealthManager,
    EmailHealthChecker,
    SMSHealthChecker,
    TelegramHealthChecker,
)
from delivery import DeliveryExecutor
from strategies import DeliveryStrategy


class NotificationService:
    """Фасад для системы уведомлений"""

    def __init__(self):
        self._initialize_components()
        self._setup_health_checks()
        self._setup_delivery_strategy()

    def _initialize_components(self):
        """Инициализирует все компоненты системы"""
        # Провайдеры
        self.providers = [EmailProvider(), SMSProvider(), TelegramProvider()]

        # Менеджеры
        self.priority_manager = PriorityManager()
        self.health_manager = HealthManager()
        self.delivery_executor = DeliveryExecutor()

    def _setup_health_checks(self):
        """Настраивает health checks"""
        self.health_manager.register_checker(EmailHealthChecker())
        self.health_manager.register_checker(SMSHealthChecker())
        self.health_manager.register_checker(TelegramHealthChecker())

    def _setup_delivery_strategy(self):
        """Настраивает стратегию доставки"""
        self.delivery_strategy = DeliveryStrategy(
            providers=self.providers,
            priority_manager=self.priority_manager,
            health_manager=self.health_manager,
            delivery_executor=self.delivery_executor,
        )

    async def send_notification(self, request: NotificationRequest) -> bool:
        """Отправляет уведомление"""
        return await self.delivery_strategy.send_notification(request)

    async def get_system_status(self) -> Dict[str, Any]:
        """Возвращает статус системы"""
        health_status = await self.health_manager.check_all_health()

        # Тестовый запрос для демонстрации плана доставки
        test_request = NotificationRequest(
            user_contact=UserContact(
                email="test@example.com",
                phone="+1234567890",
                telegram_chat_id="123456789",
            ),
            subject="Test",
            message="Test",
            priority=NotificationPriority.MEDIUM,
        )

        delivery_plan = await self.delivery_strategy.get_delivery_plan(test_request)

        return {
            "health": health_status,
            "delivery_plan": delivery_plan,
            "circuit_breaker_status": self.delivery_executor._failure_counts,
        }

    async def health_check(self) -> bool:
        """Быстрая проверка здоровья системы"""
        health_status = await self.health_manager.check_all_health()
        return health_status["overall_healthy"]

    def set_channel_priority(self, channel: NotificationType, weight: int):
        """Устанавливает приоритет канала"""
        self.priority_manager.set_channel_weight(channel, weight)
