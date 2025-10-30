from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..models.snack import Snack as SnackModel
from ..schemas.snack import Snack, SnackCreate, SnackUpdate

router = APIRouter()

@router.get("/", response_model=List[Snack])
def get_snacks(
    category: Optional[str] = Query(None, description="Filter by category"),
    vegetarian: Optional[bool] = Query(None, description="Filter vegetarian options"),
    vegan: Optional[bool] = Query(None, description="Filter vegan options"),
    available_only: bool = Query(True, description="Show only available snacks"),
    db: Session = Depends(get_db)
):
    """Get all snacks with optional filtering"""
    query = db.query(SnackModel)
    
    if available_only:
        query = query.filter(SnackModel.available == True)
    
    if category:
        query = query.filter(SnackModel.category == category)
    
    if vegetarian is not None:
        query = query.filter(SnackModel.vegetarian == vegetarian)
    
    if vegan is not None:
        query = query.filter(SnackModel.vegan == vegan)
    
    snacks = query.all()
    return snacks

@router.get("/{snack_id}", response_model=Snack)
def get_snack(snack_id: int, db: Session = Depends(get_db)):
    """Get a specific snack by ID"""
    snack = db.query(SnackModel).filter(SnackModel.id == snack_id).first()
    if not snack:
        raise HTTPException(status_code=404, detail="Snack not found")
    return snack

@router.post("/", response_model=Snack)
def create_snack(snack: SnackCreate, db: Session = Depends(get_db)):
    """Create a new snack"""
    db_snack = SnackModel(**snack.model_dump())
    db.add(db_snack)
    db.commit()
    db.refresh(db_snack)
    return db_snack

@router.put("/{snack_id}", response_model=Snack)
def update_snack(snack_id: int, snack: SnackUpdate, db: Session = Depends(get_db)):
    """Update an existing snack"""
    db_snack = db.query(SnackModel).filter(SnackModel.id == snack_id).first()
    if not db_snack:
        raise HTTPException(status_code=404, detail="Snack not found")
    
    update_data = snack.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_snack, field, value)
    
    db.commit()
    db.refresh(db_snack)
    return db_snack

@router.delete("/{snack_id}")
def delete_snack(snack_id: int, db: Session = Depends(get_db)):
    """Delete a snack"""
    db_snack = db.query(SnackModel).filter(SnackModel.id == snack_id).first()
    if not db_snack:
        raise HTTPException(status_code=404, detail="Snack not found")
    
    db.delete(db_snack)
    db.commit()
    return {"message": "Snack deleted successfully"}

@router.patch("/{snack_id}/availability")
def toggle_snack_availability(snack_id: int, available: bool, db: Session = Depends(get_db)):
    """Toggle snack availability"""
    db_snack = db.query(SnackModel).filter(SnackModel.id == snack_id).first()
    if not db_snack:
        raise HTTPException(status_code=404, detail="Snack not found")
    
    db_snack.available = available
    db.commit()
    db.refresh(db_snack)
    return {"message": f"Snack availability updated to {available}"}

@router.patch("/{snack_id}/price")
def update_snack_price(snack_id: int, price_update: dict, db: Session = Depends(get_db)):
    """Update snack price"""
    db_snack = db.query(SnackModel).filter(SnackModel.id == snack_id).first()
    if not db_snack:
        raise HTTPException(status_code=404, detail="Snack not found")
    
    if 'price' in price_update:
        db_snack.price = price_update['price']
    
    db.commit()
    db.refresh(db_snack)
    return {"message": "Snack price updated"}

@router.get("/categories/available")
def get_available_categories(db: Session = Depends(get_db)):
    """Get all available snack categories"""
    categories = db.query(SnackModel.category).filter(SnackModel.available == True).distinct().all()
    return [category[0] for category in categories]