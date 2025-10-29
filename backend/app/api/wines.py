from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from pathlib import Path

from ..core.database import get_db
from ..models.wine import Wine as WineModel
from ..schemas.wine import Wine, WineCreate, WineUpdate

router = APIRouter()

@router.get("/", response_model=List[Wine])
def get_wines(
    color: Optional[str] = Query(None, description="Filter by wine color (red, white, rosé)"),
    available_only: bool = Query(True, description="Show only available wines"),
    db: Session = Depends(get_db)
):
    """Get all wines with optional filtering"""
    query = db.query(WineModel)
    
    if available_only:
        query = query.filter(WineModel.available == True)
    
    if color:
        query = query.filter(WineModel.color == color)
    
    wines = query.all()
    return wines

@router.get("/vinos", response_model=List[Wine])
def get_vinos(db: Session = Depends(get_db)):
    """Legacy endpoint for compatibility with existing frontend"""
    wines = db.query(WineModel).filter(WineModel.available == True).all()
    return wines

@router.get("/{wine_id}", response_model=Wine)
def get_wine(wine_id: str, db: Session = Depends(get_db)):
    """Get a specific wine by ID"""
    wine = db.query(WineModel).filter(WineModel.id == wine_id).first()
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    return wine

@router.post("/", response_model=Wine)
def create_wine(wine: WineCreate, db: Session = Depends(get_db)):
    """Create a new wine"""
    # Check if wine with this ID already exists
    existing_wine = db.query(WineModel).filter(WineModel.id == wine.id).first()
    if existing_wine:
        raise HTTPException(status_code=400, detail="Wine with this ID already exists")
    
    db_wine = WineModel(**wine.model_dump())
    db.add(db_wine)
    db.commit()
    db.refresh(db_wine)
    return db_wine

@router.put("/{wine_id}", response_model=Wine)
def update_wine(wine_id: str, wine: WineUpdate, db: Session = Depends(get_db)):
    """Update an existing wine"""
    db_wine = db.query(WineModel).filter(WineModel.id == wine_id).first()
    if not db_wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    
    update_data = wine.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_wine, field, value)
    
    db.commit()
    db.refresh(db_wine)
    return db_wine

@router.delete("/{wine_id}")
def delete_wine(wine_id: str, db: Session = Depends(get_db)):
    """Delete a wine"""
    db_wine = db.query(WineModel).filter(WineModel.id == wine_id).first()
    if not db_wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    
    db.delete(db_wine)
    db.commit()
    return {"message": "Wine deleted successfully"}

@router.patch("/{wine_id}/availability")
def toggle_wine_availability(wine_id: str, available: bool, db: Session = Depends(get_db)):
    """Toggle wine availability"""
    db_wine = db.query(WineModel).filter(WineModel.id == wine_id).first()
    if not db_wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    
    db_wine.available = available
    db.commit()
    db.refresh(db_wine)
    return {"message": f"Wine availability updated to {available}"}

@router.patch("/bulk/prices")
def bulk_update_prices(updates: dict, db: Session = Depends(get_db)):
    """Bulk update wine prices"""
    updated_count = 0
    for wine_id, new_prices in updates.items():
        db_wine = db.query(WineModel).filter(WineModel.id == wine_id).first()
        if db_wine:
            db_wine.prices = new_prices
            updated_count += 1
    
    db.commit()
    return {"message": f"Updated {updated_count} wines", "count": updated_count}

@router.get("/colors/available")
def get_available_colors(db: Session = Depends(get_db)):
    """Get all available wine colors"""
    colors = db.query(WineModel.color).filter(WineModel.available == True).distinct().all()
    return [color[0] for color in colors]

@router.post("/{wine_id}/image")
async def upload_wine_image(
    wine_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload image for wine"""
    db_wine = db.query(WineModel).filter(WineModel.id == wine_id).first()
    if not db_wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    upload_dir = Path("uploads/wines")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_extension = file.filename.split(".")[-1] if file.filename else "jpg"
    file_path = upload_dir / f"{wine_id}.{file_extension}"
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    db_wine.image = str(file_path)
    db.commit()
    
    return {"message": "Image uploaded", "path": str(file_path)}