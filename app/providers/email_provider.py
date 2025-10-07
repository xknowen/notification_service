import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio

from providers.base import NotificationProvider
from models.notifications import NotificationType, NotificationRequest
from core.config import settings


class EmailProvider(NotificationProvider):
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL

    @property
    def name(self) -> str:
        return NotificationType.EMAIL

    def can_handle(self, request: NotificationRequest) -> bool:
        return bool(request.user_contact.email)

    async def send(self, request: NotificationRequest) -> bool:
        try:
            if not request.user_contact.email:
                return False

            message = MIMEMultipart()
            message["From"] = self.from_email
            message["To"] = request.user_contact.email
            message["Subject"] = request.subject

            message.attach(
                MIMEText(
                    request.message,
                    "html" if request.metadata.get("is_html") else "plain",
                )
            )

            async with aiosmtplib.AsyncSMTP(
                hostname=self.smtp_host, port=self.smtp_port, use_tls=True
            ) as smtp:
                await smtp.login(self.smtp_user, self.smtp_password)
                await smtp.send_message(message)

                print(f"Email sent to {request.user_contact.email}")
                return True

        except Exception as e:
            print(f"Email send failed: {e}")
            return False
