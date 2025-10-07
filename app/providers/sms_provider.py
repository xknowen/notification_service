import aiohttp
from providers.base import NotificationProvider
from models.notifications import NotificationRequest, NotificationType
from core.config import settings


class SMSProvider(NotificationProvider):
    def __init__(self):
        self.api_key = settings.SMS_API_KEY
        self.api_url = settings.SMS_API_URL
        self.sender = settings.SMS_SENDER

    @property
    def name(self) -> str:
        return NotificationType.SMS

    def can_handle(self, request: NotificationRequest) -> bool:
        return bool(request.user_contact.phone)

    async def send(self, request: NotificationRequest) -> bool:
        try:
            if not request.user_contact.phone:
                return False

            # Имитация отправки SMS через внешний API
            async with aiohttp.ClientSession() as session:
                payload = {
                    "api_key": self.api_key,
                    "phone": request.user_contact.phone,
                    "sender": self.sender,
                    "text": f"{request.subject}: {request.message}",
                    "priority": request.priority,
                }

                async with session.post(
                    f"{self.api_url}/send",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 200:
                        print(f"SMS sent to {request.user_contact.phone}")
                        return True
                    else:
                        print(f"SMS sending failed: {response.status}")
                        return False

        except Exception as e:
            print(f"SMS sending failed: {e}")
            return False
