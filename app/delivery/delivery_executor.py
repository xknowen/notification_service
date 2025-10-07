from typing import List
from models.notifications import NotificationRequest
from providers.base import NotificationProvider


class DeliveryExecutor:
    """Выполняет фактическую доставку уведомлений"""

    def __init__(self):
        self._max_retries_per_provider = 1
        self._circuit_breaker_threshold = 3
        self._failure_counts = {}  # Circuit breaker pattern

    async def send_via_provider(
        self, provider: NotificationProvider, request: NotificationRequest
    ) -> bool:
        """Отправляет уведомление через конкретный провайдер"""
        provider_name = provider.name

        # Проверка circuit breaker
        if self._is_circuit_open(provider_name):
            print(f"Circuit open for {provider_name}, skipping")
            return False

        try:
            success = await provider.send(request)

            if success:
                self._record_success(provider_name)
                return True
            else:
                self._record_failure(provider_name)
                return False

        except Exception as e:
            self._record_failure(provider_name)
            print(f"Error with {provider_name}: {e}")
            return False

    async def execute_delivery_chain(
        self, providers: List[NotificationProvider], request: NotificationRequest
    ) -> bool:
        """Выполняет доставку через цепочку провайдеров пока не получится"""
        if not providers:
            print("No providers available for delivery")
            return False

        print(f"Delivery chain: {[p.name for p in providers]}")

        for i, provider in enumerate(providers):
            print(f"Attempt {i+1}: {provider.name}")

            success = await self.send_via_provider(provider, request)
            if success:
                print(f"Successfully delivered via {provider.name}")
                return True
            else:
                print(f"Failed via {provider.name}, trying next...")

        print("All delivery attempts failed")
        return False

    def _record_success(self, provider_name: str):
        """Записывает успешную доставку (circuit breaker)"""
        self._failure_counts[provider_name] = 0

    def _record_failure(self, provider_name: str):
        """Записывает неудачную доставку (circuit breaker)"""
        self._failure_counts[provider_name] = (
            self._failure_counts.get(provider_name, 0) + 1
        )

    def _is_circuit_open(self, provider_name: str) -> bool:
        """Проверяет, открыт ли circuit breaker для провайдера"""
        failures = self._failure_counts.get(provider_name, 0)
        return failures >= self._circuit_breaker_threshold

    def reset_circuit(self, provider_name: str):
        """Сбрасывает circuit breaker для провайдера"""
        self._failure_counts[provider_name] = 0
