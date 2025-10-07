import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""

    # SMTP settings
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "")

    # SMS settings
    SMS_API_KEY: str = os.getenv("SMS_API_KEY", "demo-key")
    SMS_API_URL: str = os.getenv("SMS_API_URL", "https://api.sms-provider.com")
    SMS_SENDER: str = os.getenv("SMS_SENDER", "Notification")

    # Telegram settings
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "demo-token")

    # Application settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    HEALTH_CHECK_TIMEOUT: int = int(os.getenv("HEALTH_CHECK_TIMEOUT", "5"))

    class Config:
        env_file = ".env"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings()
