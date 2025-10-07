import aiohttp
from typing import Dict, Any

from health.base import HealthChecker
from core.config import settings


class TelegramHealthChecker(HealthChecker):
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

    @property
    def service_name(self) -> str:
        return "telegram_bot"

    async def check_health(self) -> Dict[str, Any]:
        """Проверяет доступность Telegram Bot API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/getMe", timeout=aiohttp.ClientTimeout(total=5)
                ) as response:

                    result = await response.json()
                    healthy = result.get("ok", False)
                    bot_info = result.get("result") if healthy else None

                    return {
                        "status": "healthy" if healthy else "unhealthy",
                        "healthy": healthy,
                        "service": self.service_name,
                        "details": {
                            "bot_username": (
                                bot_info.get("username") if bot_info else None
                            ),
                            "bot_first_name": (
                                bot_info.get("first_name") if bot_info else None
                            ),
                            "api_response": result,
                            "bot_token_configured": bool(self.bot_token),
                        },
                    }

        except aiohttp.ClientError as e:
            return {
                "status": "connection_error",
                "healthy": False,
                "error": f"Connection error: {str(e)}",
                "service": self.service_name,
                "details": {
                    "api_url": "api.telegram.org",
                    "error_type": type(e).__name__,
                },
            }
        except Exception as e:
            return {
                "status": "error",
                "healthy": False,
                "error": str(e),
                "service": self.service_name,
            }
