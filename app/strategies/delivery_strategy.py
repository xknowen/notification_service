from typing import List
from models.notifications import NotificationRequest
from providers.base import NotificationProvider
from prioritization.priority_manager import PriorityManager
from delivery.delivery_executor import DeliveryExecutor
from health.health_manager import HealthManager


class DeliveryStrategy:
    """Координирует доставку уведомлений используя отдельные менеджеры"""

    def __init__(
        self,
        providers: List[NotificationProvider],
        priority_manager: PriorityManager,
        health_manager: HealthManager,
        delivery_executor: DeliveryExecutor,
    ):

        self.providers = providers
        self.priority_manager = priority_manager
        self.health_manager = health_manager
        self.delivery_executor = delivery_executor

    async def send_notification(
        self, request: NotificationRequest, consider_health: bool = True
    ) -> bool:
        """Основной метод отправки уведомления"""

        # 1. Получаем провайдеров, отсортированных по приоритету
        all_sorted_providers = self.priority_manager.get_sorted_providers(
            self.providers, request
        )

        if not all_sorted_providers:
            print("No suitable providers for this request")
            return False

        # 2. Фильтруем по здоровью если нужно
        if consider_health:
            health_status = await self.health_manager.check_all_health()
            healthy_providers = self.health_manager.get_healthy_providers(health_status)

            # Оставляем только здоровых провайдеров, сохраняя порядок
            final_providers = [
                provider
                for provider in all_sorted_providers
                if provider.name in healthy_providers
            ]

            if not final_providers and all_sorted_providers:
                print("No healthy providers, trying all available...")
                final_providers = all_sorted_providers
        else:
            final_providers = all_sorted_providers

        # 3. Выполняем доставку
        return await self.delivery_executor.execute_delivery_chain(
            final_providers, request
        )

    async def get_delivery_plan(self, request: NotificationRequest) -> dict:
        """Возвращает план доставки без фактической отправки"""
        all_sorted_providers = self.priority_manager.get_sorted_providers(
            self.providers, request
        )

        health_status = await self.health_manager.check_all_health()
        healthy_providers = self.health_manager.get_healthy_providers(health_status)

        scores = self.priority_manager.get_provider_scores(self.providers, request)

        return {
            "all_providers_sorted": [p.name for p in all_sorted_providers],
            "healthy_providers": healthy_providers,
            "final_plan": [
                p.name for p in all_sorted_providers if p.name in healthy_providers
            ],
            "provider_scores": scores,
            "health_status": {
                k: v.get("healthy") for k, v in health_status["services"].items()
            },
        }
