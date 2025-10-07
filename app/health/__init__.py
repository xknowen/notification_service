from health.health_manager import HealthManager
from health.base import HealthChecker
from health.email_checker import EmailHealthChecker
from health.sms_checker import SMSHealthChecker
from health.telegram_checker import TelegramHealthChecker

__version__ = "1.0.0"
__all__ = [
    "HealthManager",
    "HealthChecker",
    "EmailHealthChecker",
    "SMSHealthChecker",
    "TelegramHealthChecker",
]

# Создаем синглтон для удобного использования
health_manager = HealthManager()


def setup_default_health_checks():
    """Настраивает стандартные health checkers"""
    health_manager.register_checker(EmailHealthChecker())
    health_manager.register_checker(SMSHealthChecker())
    health_manager.register_checker(TelegramHealthChecker())
    return health_manager
