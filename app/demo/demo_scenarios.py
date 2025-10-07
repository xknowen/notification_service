import asyncio
from typing import Dict, Any

from services.notification_service import NotificationService
from factories.request_factory import NotificationRequestFactory
from models import NotificationPriority, NotificationType


class DemoScenarios:
    """Демонстрационные сценарии работы системы"""

    def __init__(self, notification_service: NotificationService):
        self.service = notification_service

    async def run_health_check_demo(self) -> Dict[str, Any]:
        """Демонстрация проверки здоровья системы"""
        print("🔍 Running Health Check Demo...")

        status = await self.service.get_system_status()

        print(f"Overall System Health: {status['health']['overall_status']}")
        print("\nProvider Health Details:")
        for provider_name, health in status["health"]["services"].items():
            icon = "✅" if health.get("healthy") else "❌"
            print(f"  {icon} {provider_name}: {health.get('status')}")

        print(f"\nDelivery Plan: {' → '.join(status['delivery_plan']['final_plan'])}")

        return status

    async def run_single_channel_demo(self):
        """Демонстрация отправки через один канал"""
        print("\nRunning Single Channel Demo...")

        # Email only
        email_request = NotificationRequestFactory.create_email_notification(
            email="user@example.com",
            subject="Single Channel Test",
            message="This is an email-only notification.",
            priority=NotificationPriority.MEDIUM,
        )

        success = await self.service.send_notification(email_request)
        print(f"Email only result: {'Success' if success else 'Failed'}")

    async def run_multi_channel_demo(self):
        """Демонстрация отправки через несколько каналов"""
        print("\nRunning Multi-Channel Demo...")

        multi_request = NotificationRequestFactory.create_multi_channel_notification(
            email="user@example.com",
            phone="+1234567890",
            telegram_chat_id="123456789",
            subject="Multi-Channel Test",
            message="This notification will try multiple channels.",
            priority=NotificationPriority.HIGH,
            preferred_channels=[NotificationType.TELEGRAM, NotificationType.EMAIL],
        )

        success = await self.service.send_notification(multi_request)
        print(f"Multi-channel result: {'Success' if success else 'Failed'}")

    async def run_priority_demo(self):
        """Демонстрация работы приоритетов"""
        print("\nRunning Priority Demo...")

        # High priority - предпочтение Telegram
        high_priority_request = (
            NotificationRequestFactory.create_multi_channel_notification(
                email="user@example.com",
                phone="+1234567890",
                telegram_chat_id="123456789",
                subject="URGENT: System Update",
                message="Critical system update required immediately!",
                priority=NotificationPriority.HIGH,
            )
        )

        success = await self.service.send_notification(high_priority_request)
        print(f"High priority result: {'Success' if success else 'Failed'}")

    async def run_all_demos(self):
        """Запускает все демо-сценарии"""
        print("Starting Notification Service Demos\n")

        await self.run_health_check_demo()
        await self.run_single_channel_demo()
        await self.run_multi_channel_demo()
        await self.run_priority_demo()

        print("\nAll demos completed!")
