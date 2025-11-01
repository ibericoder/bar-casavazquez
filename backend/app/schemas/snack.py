from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class SnackBase(BaseModel):
    name: str
    price: Decimal
    category: str
    description: Optional[str] = None
    allergens: Optional[List[int]] = None
    vegetarian: bool = False
    vegan: bool = False
    available: bool = True
    image: Optional[str] = None
    neu: bool = False

class SnackCreate(SnackBase):
    pass

class SnackUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    category: Optional[str] = None
    description: Optional[str] = None
    allergens: Optional[List[int]] = None
    vegetarian: Optional[bool] = None
    vegan: Optional[bool] = None
    available: Optional[bool] = None
    image: Optional[str] = None
    neu: Optional[bool] = None

class Snack(SnackBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class SnackInDB(Snack):
    pass