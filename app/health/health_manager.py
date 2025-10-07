from typing import Dict, List, Optional
import asyncio
from health.base import HealthChecker


class HealthManager:
    """Управляет проверкой здоровья провайдеров"""

    def __init__(self):
        self.checkers: Dict[str, HealthChecker] = {}
        self._cache: Dict[str, Dict] = {}
        self._cache_ttl = 30  # seconds

    def register_checker(self, checker: HealthChecker):
        """Регистрирует health checker"""
        self.checkers[checker.service_name] = checker

    async def check_provider_health(
        self, provider_name: str, use_cache: bool = True, timeout: float = 5.0
    ) -> Dict:
        """Проверяет здоровье конкретного провайдера"""
        if use_cache and self._is_cache_valid(provider_name):
            return self._cache[provider_name]

        checker = self.checkers.get(provider_name)
        if not checker:
            return {
                "status": "unknown",
                "healthy": False,
                "error": f"No health checker for {provider_name}",
                "service": provider_name,
            }

        result = await checker.check_with_timeout(timeout)
        self._cache[provider_name] = result
        return result

    async def check_all_health(self, use_cache: bool = True) -> Dict:
        """Проверяет здоровье всех провайдеров"""
        tasks = [
            self.check_provider_health(provider_name, use_cache)
            for provider_name in self.checkers.keys()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_results = {}
        overall_healthy = True

        for provider_name, result in zip(self.checkers.keys(), results):
            if isinstance(result, Exception):
                processed_results[provider_name] = {
                    "status": "exception",
                    "healthy": False,
                    "error": str(result),
                    "service": provider_name,
                }
                overall_healthy = False
            else:
                processed_results[provider_name] = result
                if not result.get("healthy", False):
                    overall_healthy = False

        return {
            "overall_status": "healthy" if overall_healthy else "unhealthy",
            "overall_healthy": overall_healthy,
            "services": processed_results,
            "timestamp": asyncio.get_event_loop().time(),
        }

    def get_healthy_providers(self, health_results: Dict) -> List[str]:
        """Возвращает список здоровых провайдеров"""
        return [
            provider_name
            for provider_name, result in health_results["services"].items()
            if result.get("healthy", False)
        ]

    def _is_cache_valid(self, provider_name: str) -> bool:
        """Проверяет валидность кеша"""
        if provider_name not in self._cache:
            return False

        cache_time = self._cache[provider_name].get("_cache_timestamp", 0)
        current_time = asyncio.get_event_loop().time()

        return (current_time - cache_time) < self._cache_ttl

    def invalidate_cache(self, provider_name: Optional[str] = None):
        """Инвалидирует кеш"""
        if provider_name:
            self._cache.pop(provider_name, None)
        else:
            self._cache.clear()
