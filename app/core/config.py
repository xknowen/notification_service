from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # SMTP settings
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"
    FROM_EMAIL: str = "your-email@gmail.com"

    # SMS settings
    SMS_API_KEY: str = "your-sms-api-key"
    SMS_API_URL: str = "https://api.sms-provider.com"
    SMS_SENDER: str = "Notification"

    # Telegram settings
    TELEGRAM_BOT_TOKEN: str = "your-bot-token"

    class Config:
        env_file = ".env"


settings = Settings()
