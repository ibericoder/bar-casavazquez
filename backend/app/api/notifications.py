from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime

from ..core.database import get_db
from ..models.notification import Notification as NotificationModel
from ..schemas.notification import Notification, NotificationCreate, NotificationUpdate

router = APIRouter()

@router.get("/", response_model=List[Notification])
def get_notifications(
    target_page: Optional[str] = Query(None, description="Filter by target page"),
    active_only: bool = Query(True, description="Show only active notifications"),
    db: Session = Depends(get_db)
):
    """Get all notifications with optional filtering"""
    query = db.query(NotificationModel)
    
    if active_only:
        now = datetime.utcnow()
        query = query.filter(
            and_(
                NotificationModel.active == True,
                # Include notifications with no expiry or expiry in the future
                (NotificationModel.expires_at.is_(None)) | 
                (NotificationModel.expires_at > now)
            )
        )
    
    if target_page:
        query = query.filter(
            (NotificationModel.target_page == target_page) |
            (NotificationModel.target_page == "all") |
            (NotificationModel.target_page.is_(None))
        )
    
    notifications = query.order_by(NotificationModel.priority.desc(), NotificationModel.created_at.desc()).all()
    return notifications

@router.get("/{notification_id}", response_model=Notification)
def get_notification(notification_id: int, db: Session = Depends(get_db)):
    """Get a specific notification by ID"""
    notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/", response_model=Notification)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    """Create a new notification"""
    db_notification = NotificationModel(**notification.model_dump())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.put("/{notification_id}", response_model=Notification)
def update_notification(notification_id: int, notification: NotificationUpdate, db: Session = Depends(get_db)):
    """Update an existing notification"""
    db_notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    update_data = notification.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_notification, field, value)
    
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    """Delete a notification"""
    db_notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(db_notification)
    db.commit()
    return {"message": "Notification deleted successfully"}

@router.patch("/{notification_id}/status")
def toggle_notification_status(notification_id: int, active: bool, db: Session = Depends(get_db)):
    """Toggle notification active status"""
    db_notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db_notification.active = active
    db.commit()
    db.refresh(db_notification)
    return {"message": f"Notification status updated to {'active' if active else 'inactive'}"}

@router.post("/cleanup-expired")
def cleanup_expired_notifications(db: Session = Depends(get_db)):
    """Remove expired notifications"""
    now = datetime.utcnow()
    expired_notifications = db.query(NotificationModel).filter(
        and_(
            NotificationModel.expires_at.isnot(None),
            NotificationModel.expires_at <= now
        )
    ).all()
    
    count = len(expired_notifications)
    for notification in expired_notifications:
        db.delete(notification)
    
    db.commit()
    return {"message": f"Cleaned up {count} expired notifications"}