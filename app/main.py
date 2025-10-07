import asyncio
import sys

from services.notification_service import NotificationService
from demo.demo_scenarios import DemoScenarios


async def main():
    """Основная функция приложения"""
    try:
        # Инициализация сервиса
        print("Initializing Notification Service...")
        service = NotificationService()

        # Быстрая проверка здоровья
        is_healthy = await service.health_check()
        if not is_healthy:
            print("System health check failed. Some providers may not be available.")
        else:
            print("System is healthy!")

        # Запуск демо-сценариев
        demo = DemoScenarios(service)
        await demo.run_all_demos()

    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
