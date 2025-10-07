import aiosmtplib
from typing import Dict, Any

from health.base import HealthChecker
from core.config import settings


class EmailHealthChecker(HealthChecker):
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD

    @property
    def service_name(self) -> str:
        return "email_smtp"

    async def health_check(self) -> Dict[str, Any]:
        """Проверяет доступность SMTP сервера"""
        try:
            async with aiosmtplib.AsyncSMTP(
                hostname=self.smtp_host, port=self.smtp_port
            ) as smtp:
                await smtp.connect()

                # Пробуем выполнить EHLO команду
                response = await smtp.ehlo()
                ehlo_success = response.code == 250

                # Пробуем аутентификацию
                auth_success = False
                if self.smtp_user and self.smtp_password:
                    try:
                        await smtp.login(self.smtp_user, self.smtp_password)
                        auth_success = True

                    except Exception as auth_error:
                        auth_success = False
                        auth_error_msg = str(auth_error)

                else:
                    auth_success = True
                    auth_error_msg = None

                healthy = ehlo_success and auth_success

                return {
                    "status": "healthy" if healthy else "unhealthy",
                    "healthy": healthy,
                    "service": self.service_name,
                    "details": {
                        "smtp_server": f"{self.smtp_host}:{self.smtp_port}",
                        "ehlo_success": ehlo_success,
                        "authentication_success": auth_success,
                        "authentication_error": (
                            auth_error_msg if not auth_success else None
                        ),
                    },
                }

        except Exception as e:
            return {
                "status": "error",
                "healthy": False,
                "error": str(e),
                "service": self.service_name,
                "details": {
                    "smtp_server": f"{self.smtp_host}:{self.smtp_port}",
                    "error": type(e).__name__,
                },
            }
