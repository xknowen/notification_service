from abc import abstractmethod, ABC
from typing import Dict, Any
from models.notifications import NotificationRequest


class NotificationProvider(ABC):
    """Абстрактный базовый класс для всех провайдеров уведомлений"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def send(self, request: NotificationRequest) -> bool:
        pass

    @abstractmethod
    def can_handle(self, request: NotificationRequest) -> bool:
        pass

    async def health_check(self):
        """Проверка доступности провайдера"""
        return True
