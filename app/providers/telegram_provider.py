import aiohttp
from providers.base import NotificationProvider
from models.notifications import NotificationRequest, NotificationType
from core.config import settings


class TelegramProvider(NotificationProvider):
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

    @property
    def name(self) -> str:
        return NotificationType.TELEGRAM

    def can_handle(self, request: NotificationRequest) -> bool:
        return bool(request.user_contact.telegram_chat_id)

    async def send(self, request: NotificationRequest) -> bool:
        try:
            if not request.user_contact.telegram_chat_id:
                return False

            message_text = f"*{request.subject}*\n\n{request.message}"

            async with aiohttp.ClientSession() as session:
                payload = {
                    "chat_id": request.user_contact.telegram_chat_id,
                    "text": message_text,
                    "parse_mode": "Markdown",
                }

                async with session.post(
                    f"{self.api_url}/sendMessage",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    result = await response.json()

                    if result.get("ok"):
                        print(
                            f"Telegram message sent to {request.user_contact.telegram_chat_id}"
                        )
                        return True
                    else:
                        print(f"Telegram sending failed: {result}")
                        return False

        except Exception as e:
            print(f"Telegram sending failed: {e}")
            return False
