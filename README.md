# Сервис Уведомлений

Мощная и расширяемая система доставки уведомлений, построенная на Python. Поддерживает несколько каналов доставки с интеллектуальным переключением при сбоях и мониторингом состояния.

## Возможности

- **Многоканальная доставка**: Поддержка Email, SMS и Telegram уведомлений
- **Интеллектуальное переключение**: Автоматическая повторная отправка через альтернативные каналы при сбое основной доставки
- **Мониторинг состояния**: Комплексные проверки работоспособности всех провайдеров уведомлений
- **Система приоритетов**: Настраиваемые приоритеты доставки и предпочтения каналов
- **Circuit Breaker**: Встроенный шаблон Circuit Breaker для обработки сбоев провайдеров
- **Асинхронная архитектура**: Полностью асинхронная реализация для высокой производительности
- **Расширяемая архитектура**: Легкое добавление новых провайдеров уведомлений и стратегий доставки
- **CLI интерфейс**: Интерфейс командной строки для простой интеграции и тестирования

## Структура проекта
notification_service/
├── main.py # Основная точка входа приложения
├── cli.py # Интерфейс командной строки
├── requirements.txt # Зависимости Python
├── config/ # Управление конфигурацией
│ ├── init.py
│ └── settings.py
├── services/ # Основная бизнес-логика
│ ├── init.py
│ └── notification_service.py
├── factories/ # Фабрики объектов
│ ├── init.py
│ └── request_factory.py
├── demo/ # Демонстрационные сценарии
│ ├── init.py
│ └── demo_scenarios.py
├── models/ # Модели данных
│ ├── init.py
│ └── notification.py
├── providers/ # Провайдеры уведомлений
│ ├── init.py
│ ├── base.py
│ ├── email_provider.py
│ ├── sms_provider.py
│ └── telegram_provider.py
├── prioritization/ # Управление приоритетами
│ ├── init.py
│ └── priority_manager.py
├── health/ # Мониторинг состояния
│ ├── init.py
│ ├── base.py
│ ├── email_checker.py
│ ├── sms_checker.py
│ ├── telegram_checker.py
│ └── health_manager.py
├── delivery/ # Исполнение доставки
│ ├── init.py
│ └── delivery_executor.py
└── strategies/ # Стратегии доставки
├── init.py
└── delivery_strategy.py

## Установка

1. Клонируйте репозиторий:
```bash
git clone <https://github.com/xknowen/notification_service.git>
cd notification_service
```
2. Установите зависимости
```bash
pip install -r requirements.txt
```
3. Настройте переменные окружения (опционально):
Создайте файл .env в корне проекта:
```bash
# SMTP конфигурация
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# SMS конфигурация
SMS_API_KEY=your-sms-api-key
SMS_API_URL=https://api.sms-provider.com
SMS_SENDER=Notification

# Telegram конфигурация
TELEGRAM_BOT_TOKEN=your-bot-token

# Настройки приложения
LOG_LEVEL=INFO
HEALTH_CHECK_TIMEOUT=5
```

## Использование

## Основное приложение

```bash
python main.py
```

## Командная строка (CLI)
Проверка состояния системы:
```bash
python cli.py health
```

Отправка уведомления:
```bash
python cli.py send --email "user@example.com" --subject "Test" --message "Hello World" --priority high
```

Отправка многоканального уведомления:
```bash
python cli.py send --email "user@example.com" --phone "+1234567890" --telegram "123456789" --subject "Important" --message "Urgent notification" --priority high
```

## Примеры кода

## Создание и отправка уведомлений
```bash
from services import NotificationService
from factories import NotificationRequestFactory
from models import NotificationPriority

# Инициализация сервиса
service = NotificationService()

# Создание запроса на уведомление
request = NotificationRequestFactory.create_multi_channel_notification(
    email="user@example.com",
    phone="+1234567890",
    telegram_chat_id="123456789",
    subject="Важное уведомление",
    message="Это тестовое сообщение",
    priority=NotificationPriority.HIGH
)

# Отправка уведомления
success = await service.send_notification(request)
```

## Проверка состояния системы
```bash
from services import NotificationService

service = NotificationService()
status = await service.get_system_status()

print(f"Общее состояние: {status['health']['overall_status']}")
for provider, health in status['health']['services'].items():
    print(f"{provider}: {health['status']}")
```

## Компоненты системы

### Провайдеры уведомлений

EmailProvider: Отправка email через SMTP
SMSProvider: Отправка SMS через внешний API
TelegramProvider: Отправка сообщений через Telegram Bot API

### Менеджеры

PriorityManager: Управление приоритетами доставки
HealthManager: Мониторинг состояния провайдеров
DeliveryExecutor: Исполнение доставки с Circuit Breaker

### Стратегии

DeliveryStrategy: Координация доставки через различные каналы

### Принципы работы

1. Приоритизация: Система оценивает доступные каналы и выбирает оптимальный на основе приоритета запроса и предпочтений пользователя
2. Резервирование: При сбое доставки через основной канал автоматически пробуются альтернативные каналы
3. Мониторинг: Регулярные проверки работоспособности всех провайдеров
4. Защита от сбоев: Circuit Breaker предотвращает многократные попытки отправки через неработающие каналы

### Расширение системы

Для добавления нового провайдера уведомлений:

1. Создайте класс, наследуемый от NotificationProvider
2. Реализуйте методы send() и can_handle()
3. Создайте соответствующий HealthChecker
4. Зарегистрируйте провайдер в NotificationService