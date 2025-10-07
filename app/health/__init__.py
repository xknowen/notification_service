from typing import Dict, Any, List
import asyncio

from base import HealthChecker
from email_checker import EmailHealthChecker
from sms_checker import SMSHealthChecker
from telegram_checker import TelegramHealthChecker


class HealthCheckManager:
    """Менеджер для управления всеми health checks"""

    def __init__(self):
        self.checkers: List[HealthChecker] = [
            EmailHealthChecker(),
            SMSHealthChecker(),
            TelegramHealthChecker(),
        ]

    def register_checker(self, checker: HealthChecker):
        """Регистрирует новый health checker"""
        self.checkers.append(checker)

    async def check_all(self, timeout_per_check: float = 5.0) -> Dict[str, Any]:
        """Выполняет все health checks параллельно"""
        tasks = [
            checker.check_with_timeout(timeout_per_check) for checker in self.checkers
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Обрабатываем результаты
        processed_results = {}
        overall_healthy = True

        for i, result in enumerate(results):
            checker_name = self.checkers[i].service_name

            if isinstance(result, Exception):
                processed_results[checker_name] = {
                    "status": "exception",
                    "healthy": False,
                    "error": str(result),
                    "service": checker_name,
                }
                overall_healthy = False
            else:
                processed_results[checker_name] = result
                if not result.get("healthy", False):
                    overall_healthy = False

        return {
            "overall_status": "healthy" if overall_healthy else "unhealthy",
            "overall_healthy": overall_healthy,
            "services": processed_results,
            "timestamp": asyncio.get_event_loop().time(),
        }

    async def check_specific(
        self, service_name: str, timeout: float = 5.0
    ) -> Dict[str, Any]:
        """Проверяет конкретный сервис"""
        for checker in self.checkers:
            if checker.service_name == service_name:
                return await checker.check_with_timeout(timeout)

        return {
            "status": "not_found",
            "healthy": False,
            "error": f"Health checker for service '{service_name}' not found",
            "service": service_name,
        }


# Синглтон для удобного использования
health_manager = HealthCheckManager()
