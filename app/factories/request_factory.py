from models import (
    NotificationRequest,
    UserContact,
    NotificationPriority,
    NotificationType,
)
from typing import Optional, List


class NotificationRequestFactory:
    """Фабрика для создания запросов на уведомления"""

    @staticmethod
    def create_email_notification(
        email: str,
        subject: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        is_html: bool = False,
    ) -> NotificationRequest:
        """Создает запрос для email уведомления"""
        return NotificationRequest(
            user_contact=UserContact(email=email),
            subject=subject,
            message=message,
            priority=priority,
            preferred_channels=[NotificationType.EMAIL],
            metadata={"is_html": is_html},
        )

    @staticmethod
    def create_sms_notification(
        phone: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.HIGH,
    ) -> NotificationRequest:
        """Создает запрос для SMS уведомления"""
        return NotificationRequest(
            user_contact=UserContact(phone=phone),
            subject="SMS Notification",  # SMS обычно без subject
            message=message,
            priority=priority,
            preferred_channels=[NotificationType.SMS],
        )

    @staticmethod
    def create_telegram_notification(
        chat_id: str,
        subject: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
    ) -> NotificationRequest:
        """Создает запрос для Telegram уведомления"""
        return NotificationRequest(
            user_contact=UserContact(telegram_chat_id=chat_id),
            subject=subject,
            message=message,
            priority=priority,
            preferred_channels=[NotificationType.TELEGRAM],
        )

    @staticmethod
    def create_multi_channel_notification(
        email: Optional[str] = None,
        phone: Optional[str] = None,
        telegram_chat_id: Optional[str] = None,
        subject: str = "Notification",
        message: str = "",
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        preferred_channels: Optional[List[NotificationType]] = None,
    ) -> NotificationRequest:
        """Создает запрос для мульти-канального уведомления"""
        return NotificationRequest(
            user_contact=UserContact(
                email=email, phone=phone, telegram_chat_id=telegram_chat_id
            ),
            subject=subject,
            message=message,
            priority=priority,
            preferred_channels=preferred_channels,
        )
