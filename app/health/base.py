from abc import abstractmethod, ABC
from typing import Any, Dict, Optional
import asyncio


class HealthChecker(ABC):
    """Абстрактный базовый класс для всех health checkers"""

    @property
    @abstractmethod
    def service_name(self) -> str:
        """Имя сервиса для проверки"""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        Проверяет здоровье сервиса

        Returns: dict с результатами проверки
        """
        pass

    @abstractmethod
    async def check_with_timeout(self, timeout: float = 5.0) -> Dict[str, Any]:
        """Выполняет проверку с таймаутом"""
        try:
            return await asyncio.wait_for(self.health_check(), timeout=timeout)

        except asyncio.TimeoutError:
            return {
                "status": "timeout",
                "health": False,
                "error": f"Health check timed out after {timeout}s",
                "service": self.service_name,
            }

        except Exception as e:
            return {
                "status": "error",
                "health": False,
                "error": str(e),
                "service": self.service_name,
            }
