import asyncio
import argparse
from services.notification_service import NotificationService
from factories.request_factory import NotificationRequestFactory
from models.notifications import NotificationPriority


async def send_notification(args):
    """Отправляет уведомление через CLI"""
    service = NotificationService()

    request = NotificationRequestFactory.create_multi_channel_notification(
        email=args.email,
        phone=args.phone,
        telegram_chat_id=args.telegram,
        subject=args.subject,
        message=args.message,
        priority=NotificationPriority(args.priority),
    )

    success = await service.send_notification(request)
    print(f"Result: {'✅ Success' if success else '❌ Failed'}")
    return 0 if success else 1


async def check_health(args):
    """Проверяет здоровье системы"""
    service = NotificationService()
    status = await service.get_system_status()

    print(f"Overall Status: {status['health']['overall_status']}")
    for provider, health in status["health"]["services"].items():
        print(f"{provider}: {health['status']}")

    return 0 if status["health"]["overall_healthy"] else 1


def main():
    parser = argparse.ArgumentParser(description="Notification Service CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Send command
    send_parser = subparsers.add_parser("send", help="Send notification")
    send_parser.add_argument("--email", help="Email address")
    send_parser.add_argument("--phone", help="Phone number")
    send_parser.add_argument("--telegram", help="Telegram chat ID")
    send_parser.add_argument("--subject", required=True, help="Notification subject")
    send_parser.add_argument("--message", required=True, help="Notification message")
    send_parser.add_argument(
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Notification priority",
    )

    # Health command
    health_parser = subparsers.add_parser("health", help="Check system health")

    args = parser.parse_args()

    if args.command == "send":
        return asyncio.run(send_notification(args))
    elif args.command == "health":
        return asyncio.run(check_health(args))


if __name__ == "__main__":
    exit(main())
