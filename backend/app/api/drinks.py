from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..models.drink import Drink as DrinkModel
from ..schemas.drink import Drink, DrinkCreate, DrinkUpdate

router = APIRouter()

@router.get("/", response_model=List[Drink])
def get_drinks(
    category: Optional[str] = Query(None, description="Filter by category"),
    alcoholic: Optional[bool] = Query(None, description="Filter by alcoholic/non-alcoholic"),
    available_only: bool = Query(True, description="Show only available drinks"),
    db: Session = Depends(get_db)
):
    """Get all drinks with optional filtering"""
    query = db.query(DrinkModel)
    
    if available_only:
        query = query.filter(DrinkModel.available == True)
    
    if category:
        query = query.filter(DrinkModel.category == category)
    
    if alcoholic is not None:
        query = query.filter(DrinkModel.alcoholic == alcoholic)
    
    drinks = query.all()
    return drinks

@router.get("/{drink_id}", response_model=Drink)
def get_drink(drink_id: int, db: Session = Depends(get_db)):
    """Get a specific drink by ID"""
    drink = db.query(DrinkModel).filter(DrinkModel.id == drink_id).first()
    if not drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    return drink

@router.post("/", response_model=Drink)
def create_drink(drink: DrinkCreate, db: Session = Depends(get_db)):
    """Create a new drink"""
    db_drink = DrinkModel(**drink.model_dump())
    db.add(db_drink)
    db.commit()
    db.refresh(db_drink)
    return db_drink

@router.put("/{drink_id}", response_model=Drink)
def update_drink(drink_id: int, drink: DrinkUpdate, db: Session = Depends(get_db)):
    """Update an existing drink"""
    db_drink = db.query(DrinkModel).filter(DrinkModel.id == drink_id).first()
    if not db_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    
    update_data = drink.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_drink, field, value)
    
    db.commit()
    db.refresh(db_drink)
    return db_drink

@router.delete("/{drink_id}")
def delete_drink(drink_id: int, db: Session = Depends(get_db)):
    """Delete a drink"""
    db_drink = db.query(DrinkModel).filter(DrinkModel.id == drink_id).first()
    if not db_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    
    db.delete(db_drink)
    db.commit()
    return {"message": "Drink deleted successfully"}

@router.patch("/{drink_id}/availability")
def toggle_drink_availability(drink_id: int, available: bool, db: Session = Depends(get_db)):
    """Toggle drink availability"""
    db_drink = db.query(DrinkModel).filter(DrinkModel.id == drink_id).first()
    if not db_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    
    db_drink.available = available
    db.commit()
    db.refresh(db_drink)
    return {"message": f"Drink availability updated to {available}"}

@router.patch("/{drink_id}/price")
def update_drink_price(drink_id: int, price_update: dict, db: Session = Depends(get_db)):
    """Update drink price"""
    db_drink = db.query(DrinkModel).filter(DrinkModel.id == drink_id).first()
    if not db_drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    
    if 'price' in price_update:
        db_drink.price = price_update['price']
    
    db.commit()
    db.refresh(db_drink)
    return {"message": "Drink price updated"}

@router.get("/categories/available")
def get_available_categories(db: Session = Depends(get_db)):
    """Get all available drink categories"""
    categories = db.query(DrinkModel.category).filter(DrinkModel.available == True).distinct().all()
    return [category[0] for category in categories]