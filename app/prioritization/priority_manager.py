from typing import List, Dict
from models.notifications import (
    NotificationRequest,
    NotificationPriority,
    NotificationType,
)
from providers.base import NotificationProvider


class PriorityManager:
    """Управляет приоритетами и сортировкой провайдеров"""

    def __init__(self):
        self._channel_weights = {
            NotificationType.TELEGRAM: 30,
            NotificationType.SMS: 20,
            NotificationType.EMAIL: 10,
        }

        self._priority_weights = {
            NotificationPriority.HIGH: 3,
            NotificationPriority.MEDIUM: 2,
            NotificationPriority.LOW: 1,
        }

    def set_channel_weight(self, channel: NotificationType, weight: int):
        """Устанавливает вес для канала уведомлений"""
        self._channel_weights[channel] = weight

    def calculate_provider_score(
        self, provider: NotificationProvider, request: NotificationRequest
    ) -> int:
        """Вычисляет скоринг провайдера для конкретного запроса"""
        score = 0

        # Базовый приоритет из запроса
        score += self._priority_weights[request.priority]

        # Вес канала
        channel_weight = self._channel_weights.get(provider.name, 0)
        score += channel_weight

        # Бонус за предпочтительные каналы
        if request.preferred_channels and provider.name in request.preferred_channels:
            score += 50  # Значительный бонус

        # Штраф за неподдерживаемые контакты
        if not provider.can_handle(request):
            score = -1  # Полностью исключаем

        return score

    def get_sorted_providers(
        self, providers: List[NotificationProvider], request: NotificationRequest
    ) -> List[NotificationProvider]:
        """Возвращает отсортированный список провайдеров по приоритету"""
        scored_providers = []

        for provider in providers:
            score = self.calculate_provider_score(provider, request)
            if score >= 0:  # Только поддерживаемые провайдеры
                scored_providers.append((provider, score))

        # Сортируем по убыванию скоринга
        scored_providers.sort(key=lambda x: x[1], reverse=True)

        return [provider for provider, score in scored_providers]

    def get_provider_scores(
        self, providers: List[NotificationProvider], request: NotificationRequest
    ) -> Dict[str, int]:
        """Возвращает детальную информацию о скоринге (для отладки)"""
        return {
            provider.name: self.calculate_provider_score(provider, request)
            for provider in providers
        }
