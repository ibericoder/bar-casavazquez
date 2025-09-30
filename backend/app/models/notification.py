from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from ..core.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, default="info")  # 'info', 'warning', 'success', 'error'
    active = Column(Boolean, default=True, nullable=False)
    priority = Column(Integer, default=0)  # Higher number = higher priority
    
    # Optional targeting
    target_page = Column(String, nullable=True)  # 'wine', 'drinks', 'snacks', 'all'
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, title='{self.title}', active={self.active})>"