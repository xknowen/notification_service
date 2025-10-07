from pydantic import BaseModel, EmailStr
from typing import Any, Optional, List, Dict
from enum import Enum


class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    Telegram = "telegram"


class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UserContact(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    telegram_id: Optional[str] = None


class NotificationRequest(BaseModel):
    user_contact = UserContact
    subject: str
    message: str
    priority: NotificationPriority = NotificationPriority.MEDIUM
    preferred_channels: List[NotificationType] = None
    metadata: Dict[str, any] = {}
