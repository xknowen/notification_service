import aiohttp
from typing import Dict, Any

from health.base import HealthChecker
from core.config import settings


class SMSHealthChecker(HealthChecker):
    def __init__(self):
        self.api_key = settings.SMS_API_KEY
        self.api_url = settings.SMS_API_URL

    @property
    def service_name(self) -> str:
        return "sms_provider"

    async def health_check(self) -> Dict[str, Any]:
        """Проверяет доступность sms провайдера"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/health",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:

                    healthy = response.status == 200
                    response_data = await response.json() if healthy else None

                    return {
                        "status": "healthy" if healthy else "unhealthy",
                        "healthy": healthy,
                        "service": self.service_name,
                        "details": {
                            "api_url": self.api_url,
                            "http_status": response.status,
                            "response_data": response_data,
                            "api_key_configured": bool(self.api_key),
                        },
                    }

        except aiohttp.ClientError as e:
            return {
                "status": "connection_error",
                "healthy": False,
                "service": self.service_name,
                "details": {"api_url": self.api_url, "eroor_type": type(e).__name__},
            }

        except Exception as e:
            return {
                "status": "error",
                "healthy": False,
                "error": str(e),
                "service": self.service_name,
            }
