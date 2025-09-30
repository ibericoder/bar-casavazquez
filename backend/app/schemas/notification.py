from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    title: str
    message: str
    type: str = "info"
    active: bool = True
    priority: int = 0
    target_page: Optional[str] = None
    expires_at: Optional[datetime] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    type: Optional[str] = None
    active: Optional[bool] = None
    priority: Optional[int] = None
    target_page: Optional[str] = None
    expires_at: Optional[datetime] = None

class Notification(NotificationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class NotificationInDB(Notification):
    pass